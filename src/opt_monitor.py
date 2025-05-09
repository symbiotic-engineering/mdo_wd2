import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from openmdao.recorders.case_reader import CaseReader

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
    best_per_gen = []

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

                best_per_gen.append(gen_best)

                if gen_best < best_so_far - 1e-3:
                    best_so_far = gen_best
                    patience_counter = 0
                    print(f"[Gen {gen:>3}] New best LCOW: {best_so_far:.6f}")
                else:
                    patience_counter += 1
                    print(f"[Gen {gen:>3}] Best LCOW: {gen_best:.6f} (no improvement)")

                plot_progress(best_per_gen)  # update the plot

            last_idx += (gen * pop_size)

        time.sleep(check_interval)


def plot_progress(best_per_gen, filename="lcow_progress.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(best_per_gen, marker='o', linestyle='-', color='blue')
    plt.xlabel("Generation")
    plt.ylabel("Best LCOW")
    plt.title("LCOW Optimization Progress")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":
    monitor_optimization(casefile="run1_robustoptrun_out/cases.sql", pop_size=80)
