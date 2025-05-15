import os
import time
import csv
import matplotlib.pyplot as plt
import ast

def monitor_csv(csv_path="results.csv", check_interval=5, patience=20, tol=1e-3):
    # Initialize variables
    best_so_far = float('inf')
    best_per_gen = []
    stagnation_counter = 0
    last_gen_processed = -1

    print("Monitoring optimization progress (Ctrl+C to stop)...\n")

    while True:
        # Check if the CSV file exists
        if not os.path.exists(csv_path):
            print(f"Waiting for '{csv_path}' to be created...")
            time.sleep(2)
            continue

        # Read the latest rows from the CSV file
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Extract all generations present
        gen_fitnesses = {}
        for row in rows:
            gen = int(row['generation'])
            fitness_str = row['fitness'].strip()
            try:
                # Handle '[nan]' or 'nan'
                if 'nan' in fitness_str.lower():
                    fitness = float('nan')
                elif fitness_str.startswith('[') and fitness_str.endswith(']'):
                    fitness = float(fitness_str.strip('[]'))
                else:
                    fitness = float(fitness_str)
            except Exception as e:
                print(f"Could not parse fitness value '{fitness_str}': {e}")
                continue  # Skip this row
            if gen not in gen_fitnesses:
                gen_fitnesses[gen] = []
            gen_fitnesses[gen].append(fitness)

        # Process only new generations
        sorted_gens = sorted(gen for gen in gen_fitnesses if gen > last_gen_processed)
        for gen in sorted_gens:
            gen_best = min(gen_fitnesses[gen])
            best_per_gen.append(gen_best)

            if abs((gen_best-best_so_far)/gen_best) > tol:
                best_so_far = gen_best
                stagnation_counter = 0
                print(f"[Gen {gen:>3}] New best fitness: {best_so_far:.6f}")
            else:
                stagnation_counter += 1
                print(f"[Gen {gen:>3}] Best fitness: {gen_best:.6f} (no improvement)")

            plot_progress(best_per_gen)
            last_gen_processed = gen

            #if stagnation_counter >= patience:
            #    print(f"Early stopping at Gen {gen}. No improvement in {patience} generations.")
            #    return

        time.sleep(check_interval)

def plot_progress(best_per_gen, filename="optimization_progress.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(best_per_gen, marker='o', linestyle='-', color='blue')
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Optimization Progress")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    monitor_csv(csv_path="data/results.csv", check_interval=5)
