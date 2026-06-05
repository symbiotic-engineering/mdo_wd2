import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.params import PARAMS, INPUTS, OPTIMAL_4
from src.runner import RunWDDS
os.environ["TMPDIR"] = "~/scratch/matlab_tmp"
os.makedirs("~/scratch/matlab_tmp", exist_ok=True)

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
#eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.initializematlab(0,nargout=0)
eng.cd('..', nargout=0)

Runner = RunWDDS(eng)
Runner.create_problem()
design = OPTIMAL_4
#design["width"] = 9.5
#design["thickness"] = 0.95
lcow = Runner.solve_once(design_variables=design)
print(lcow)