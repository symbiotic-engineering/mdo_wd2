import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import time
from openmdao.recorders.case_reader import CaseReader
import os
import numpy as np

def monitor_optimization(casefile="robustoptrun_out/cases.sql", pop_size=80, check_interval=10):
    if not os.path.exists(casefile):
        print(f"No case file found at '{casefile}'. Waiting for it to be created...")
        while not os.path.exists(casefile):
            time.sleep(2)

    cr = CaseReader(casefile)
    all_cases = cr.get_cases('driver', recurse=False)

    last_idx = 0
    gen = 0
    best_so_far = float('inf')
    patience_counter = 0
    patience = 15  # match your optimization setting

    print("Monitoring optimization progress by generation (Ctrl+C to stop)...\n")

    while True:
        all_cases = cr.get_cases('driver', recurse=False)
        new_cases = all_cases[last_idx:]
        num_new = len(new_cases)

        if num_new >= pop_size:
            for i in range(0, num_new, pop_size):
                gen_cases = new_cases[i:i+pop_size]
                if len(gen_cases) < pop_size:
                    break  # partial gen, wait for more

                gen += 1
                gen_best = float('inf')
                for case in gen_cases:
                    val = case.outputs['LCOW']
                    val = float(val) if np.isscalar(val) else float(val[0])
                    gen_best = min(gen_best, val)

                if gen_best < best_so_far - 1e-3:
                    best_so_far = gen_best
                    patience_counter = 0
                    print(f"[Gen {gen:>3}] New best LCOW: {best_so_far:.6f}")
                else:
                    patience_counter += 1
                    print(f"[Gen {gen:>3}] Best LCOW: {gen_best:.6f} (no improvement)")

            last_idx += (gen * pop_size)

        time.sleep(check_interval)

if __name__ == "__main__":
    monitor_optimization(casefile="robustoptrun_out/cases.sql", pop_size=80)