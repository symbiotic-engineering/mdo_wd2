import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import capytaine as capy
import numpy as np
import xarray as xr
import src.hydro.hydro as hydro
import src.systemdynamics.sysdyn as sysdyn
import src.econ.econ as econ
from src.params import PARAMS
import matlab.engine
import time

print("Starting MATLAB Engine...")
start_time = time.time()
future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()
end_time = time.time()
print(f"MATLAB Engine Started in {end_time-start_time} seconds.")

initialization_script_path = "/home/degoede/SEA/mdo_wd2/src/"
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

w = 18
t = 1
h = 10
draft = 9
cog = -0.7 * h
hydroins = {    
    'width': w,
    'thickness': t,
    'height': h,
    'draft': draft,
    'center_of_gravity': cog
}
hydroouts = {}
Hydro = hydro.Hydro()
Hydro.setup()
print('Starting BEM...')
start_time = time.time()
Hydro.compute(hydroins, hydroouts)
end_time = time.time()
print(f'BEM Completed in {end_time-start_time} seconds.')

sysdynins = {
    "added_mass": hydroouts["added_mass"],
    "radiation_damping": hydroouts["radiation_damping"],
    "sc_re": hydroouts["sc_re"],
    "sc_im": hydroouts["sc_im"],
    "fk_re": hydroouts["fk_re"],
    "fk_im": hydroouts["fk_im"],
    "ex_re": hydroouts["ex_re"],
    "ex_im": hydroouts["ex_im"],
    "hydrostatic_stiffness": hydroouts["hydrostatic_stiffness"],

    "wec_mass": 127000.0,
    "inertia_matrix": np.array([[1.85e6]]),
    "Vo": w*t*draft,
    "draft": draft,
    "cog": cog,
    "thickness": t,

    "hinge_depth": 8.9,
    "joint_depth": 7.0,
    "intake_x": 4.7,
    "drivetrain_mass": 50.0,

    "piston_area": 0.26,
    "piston_stroke": 12.0,
    "accum_volume": 4.0,
    "accum_P0": 3.0,
    "pressure_relief": 6.0,
    "throt_resist": 60.23,
    
    "mem_resist": 60.23,
    "osmotic_pressure": 3.0,
}

print('Starting System Dynamics...')
start_time = time.time()
sysdynouts = {}
SysDyn = sysdyn.SysDyn()
SysDyn.setup(eng)
SysDyn.compute(sysdynins, sysdynouts)
end_time = time.time()
print(f'System Dynamics Completed in {end_time-start_time} seconds.')

print('Starting System Dynamics for the 2nd time...')
start_time = time.time()
sysdynouts = {}
SysDyn = sysdyn.SysDyn()
SysDyn.setup(eng)
SysDyn.compute(sysdynins, sysdynouts)
end_time = time.time()
print(f'System Dynamics Completed in {end_time-start_time} seconds the 2nd time.')

econins = {
    'feedflow_cap': 6000.0,
    'permflow_cap': 3000.0,
    'feedflow': sysdynouts['feedflow'],
    'permflow': sysdynouts['permflow'],
}

print('Starting Economics...')
start_time = time.time()
econouts = {}
Econ = econ.Econ()
Econ.setup()
Econ.compute(econins, econouts)
end_time = time.time()
print(f'Economics Completed in {end_time-start_time} seconds.')
print('---------------------------------')
print(f"LCOW: {econouts['LCOW']} $/m^3")