import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.runner import RunWDDS
from src.DEAPSEA.src.ga import DeapSeaGa as GA
from src.cleaning import start_cleanup_thread
from src.params import PARAMS, BOUNDS, BITS, IDETC, OPTIMAL
from threadpoolctl import threadpool_limits
threadpool_limits(limits=1, user_api='blas')
threadpool_limits(limits=1, user_api='openmp')
os.environ["TMPDIR"] = "~/scratch/matlab_tmp"
os.makedirs("~/scratch/matlab_tmp", exist_ok=True)

start_cleanup_thread()

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def objective(ind):
    Runner = RunWDDS(eng)
    Runner.create_problem()
    LCOW = Runner.solve_once(ind)
    return (LCOW,)

def safe_objective(ind):
    try:
        return objective(ind)
    except Exception as e:
        print(f"Error in objective function: {e}")
        return (np.inf,)  # Return a large value to indicate failure

ga = GA(safe_objective, BOUNDS, BITS, 
        NGEN=800, NPOP=400, NWORKERS=PARAMS["nworkers"],
        CXPB=0.8, MUTPB=0.20, ELITES_SIZE=1, TOURNAMENT_SIZE=2,
        NIMMIGRANTS=300, IMMIGRATION_INTERVAL=50,
        PATIENCE=100, TOL=1e-3, csv_path="data/newresults_apocalypse.csv")
design,lcow = ga.run(initial_design=IDETC)
print("Best design:", design)
print("Best LCOW:", lcow)

print("Optimization complete.")
eng.quit()
