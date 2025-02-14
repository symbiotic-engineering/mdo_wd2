import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import capytaine as capy
import numpy as np
import xarray as xr
import src.hydro.hydro as hydro
import src.systemdynamics.sysdyn as sysdyn
from src.params import PARAMS
import matlab.engine

future_eng = matlab.engine.start_matlab(background=True)

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
Hydro.compute(hydroins, hydroouts)
print('BEM Complete.')

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

    "piston_area": 0.26,
    "piston_stroke": 12.0,
    "accum_volume": 4.0,
    "accum_P0": 30.0,
    "pressure_relief": 60.0,
    "throt_resist": 60.23,
    "mem_resist": 60.23,
    "mem_pressure_min": 30.0,
    "drivetrain_mass": 50.0,
}

print('Starting System Dynamics...')
sysdynouts = {}
SysDyn = sysdyn.SysDyn()
eng = future_eng.result()
eng.run('/home/degoede/SEA/mdo_wd2/src/initializematlab.m',nargout=0)
SysDyn.setup(eng)
SysDyn.compute(sysdynins, sysdynouts)
print('System Dynamics Complete.')