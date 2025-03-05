import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import src.model as model
import matlab.engine
from src.params import PARAMS, INPUTS
from src.runner import RunWDDS

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = "/home/degoede/SEA/mdo_wd2/src/"
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

result = model.run_sim(INPUTS,eng)
print(result)
Runner = RunWDDS(eng)
Runner.create_problem()
lcow = Runner.solve_once()
print(lcow)