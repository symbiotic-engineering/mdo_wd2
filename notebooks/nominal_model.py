import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import src.model as model
import matlab.engine
from src.params import PARAMS

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = "/home/degoede/SEA/mdo_wd2/src/"
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

inputs = {
    # WEC Params
    'w' : 18,
    't' : 1.0,
    'draft' : 9,
    'cog' : -0.7 * 10,
    'wec_mass' : 127000.0,
    'inertia_matrix' : np.array([[1.85e6]]),

    # Mechanism Params
    'joint_depth' : 7.0,
    'intake_x' : 4.7,

    # Hydraulic Params
    'piston_area' : 0.26,
    'piston_stroke' : 12.0,
    'accum_volume' : 4.0,
    'accum_P0' : 3.0,

    # Desal Params
    'capacity' : 6000,
}

result = model.run_sim(inputs,eng)
print(result)