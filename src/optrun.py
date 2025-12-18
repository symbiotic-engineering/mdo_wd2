import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.runner import RunWDDS
from src.DEAPSEA.src.ga import DeapSeaGa as GA
from src.params import PARAMS, BOUNDS, BITS, IDETC, OPTIMAL
from threadpoolctl import threadpool_limits
threadpool_limits(limits=1, user_api='blas')
threadpool_limits(limits=1, user_api='openmp')
import argparse

parser = argparse.ArgumentParser(description="Run optimization with wave parameters.")
parser.add_argument("--wave_height", type=float, default=PARAMS["significant_wave_height"],
                    help="Significant wave height (default uses value from params.py)")
parser.add_argument("--peak_period", type=float, default=PARAMS["peak_period"],
                    help="Peak period (default uses value from params.py)")
args = parser.parse_args()

# Update PARAMS
PARAMS["significant_wave_height"] = args.wave_height
PARAMS["peak_period"] = args.peak_period

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def objective(ind):
    Runner = RunWDDS(eng)
    Runner.create_problem(significant_wave_height=PARAMS["significant_wave_height"], peak_period=PARAMS["peak_period"])
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
        PATIENCE=20, TOL=1e-3, csv_path="data/newresults.csv")
print(ga.run(initial_design=OPTIMAL))
print("Optimization complete.")
eng.quit()
