import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.runner import RunWDDS
from src.DEAPSEA.src.ga import DeapSeaGa as GA
from src.params import PARAMS, BOUNDS, BITS, OPTIMAL
from threadpoolctl import threadpool_limits
threadpool_limits(limits=1, user_api='blas')
threadpool_limits(limits=1, user_api='openmp')

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

seastates = [{"Hs": 2.5, "Tp": 10.0}]

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def run_optimization(Hs, Tp, initial_design=None):
    def objective(ind):
        Runner = RunWDDS(eng)
        Runner.create_problem(significant_wave_height=Hs, peak_period=Tp)
        LCOW = Runner.solve_once(ind)
        return (LCOW,)

    def safe_objective(ind):
        try:
            return objective(ind)
        except Exception as e:
            print(f"Error in objective function: {e}")
            return (np.inf,)  # Return a large value to indicate failure

    ga = GA(safe_objective, BOUNDS, BITS, 
            NGEN=800, NPOP=256, NWORKERS=PARAMS["nworkers"],
            CXPB=0.8, MUTPB=0.02, ELITES_SIZE=3, TOURNAMENT_SIZE=4,
            PATIENCE=20, TOL=1e-3, csv_path=f"data/sensitivity/results_{Hs:.2f}m_{Tp:.2f}s.csv")
    design, lcow = ga.run(initial_design=initial_design)
    return design, lcow

def find_nearest_design(seastate, completed):
    Hs_target, Tp_target = seastate["Hs"], seastate["Tp"]

    # Initialize
    min_dist = float("inf")
    nearest_design = None

    # Loop through all completed optimizations
    for entry in completed:
        Hs, Tp = entry["Hs"], entry["Tp"]
        # Euclidean distance in (Hs, Tp) space
        dist = ((Hs - Hs_target)**2 + (Tp - Tp_target)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            nearest_design = entry["design"]

    return nearest_design

completed = [{"Hs": 2.64, "Tp": 9.86, "design": OPTIMAL}]
for seastate in seastates:
    print(f"Running optimization for Hs={seastate['Hs']} m, Tp={seastate['Tp']} s")
    nearest_result = find_nearest_design(seastate, completed)
    design, lcow = run_optimization(Hs=seastate['Hs'], Tp=seastate['Tp'], initial_design=nearest_result)
    results = {"Hs": seastate["Hs"], "Tp": seastate["Tp"], "design": design}
    completed.append(results)
    print(f"Best design for Hs={seastate['Hs']} m, Tp={seastate['Tp']} s: {design} with LCOW={lcow}")


eng.quit()
