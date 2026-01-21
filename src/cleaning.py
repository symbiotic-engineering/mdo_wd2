import os
import shutil
import time
import threading

def clean_simscape_tmp(TMP, threshold_gb=50, interval=30):
    """
    Auto-clean MATLAB/Simscape temporary files in TMPDIR while optimization runs.
    threshold_gb: clean when TMPDIR exceeds this size.
    interval: seconds between checks.
    """
    def folder_size(path):
        total = 0
        for root, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total += os.path.getsize(fp)
                except FileNotFoundError:
                    pass
        return total

    while True:
        try:
            size_bytes = folder_size(TMP)
            size_gb = size_bytes / 1e9

            if size_gb > threshold_gb:
                print(f"[CLEANUP] {TMP} is {size_gb:.1f} GB. Cleaning MATLAB/Simscape temp files...")

                for item in os.listdir(TMP):
                    p = os.path.join(TMP, item)

                    # remove WEC-Sim / MATLAB temp files
                    if (
                        item.startswith("__mw_qi_") or
                        item.startswith("matlab_") or
                        item.startswith("mwd") or
                        item.startswith("Java") or
                        item.startswith("ssc_sli") or
                        item.endswith(".tmp") or
                        item.endswith(".dmr")
                    ):
                        try:
                            if os.path.isdir(p):
                                shutil.rmtree(p, ignore_errors=True)
                            else:
                                os.remove(p)
                        except Exception:
                            pass

            time.sleep(interval)

        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")
            time.sleep(interval)

def start_cleanup_thread(folder):
    # Use the same TMPDIR that MATLAB sees
    TMP = os.path.expanduser(os.environ.get("TMPDIR",folder))
    t = threading.Thread(target=clean_simscape_tmp, args=(TMP,), daemon=True)
    t.start()
