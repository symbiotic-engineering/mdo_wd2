import capytaine as capy
import numpy as np
import xarray as xr
import src.hydro.hydro as hydro
import src.systemdynamics.sysdyn as sysdyn
import src.econ.econ as econ
import src.desal.desal as desal
from src.params import PARAMS

def run_sim(inputs,eng):
    hydroins = {    
        'width': inputs["w"],
        'thickness': inputs["t"],
        'draft': inputs["draft"],
        'center_of_gravity': inputs["cog"],
    }

    hydroouts = {}
    Hydro = hydro.Hydro()
    Hydro.setup()
    Hydro.compute(hydroins, hydroouts)

    desalins = {
        'capacity': inputs["capacity"]
    }

    desalouts = {}
    DesalParams = desal.DesalParams()
    DesalParams.setup()
    DesalParams.compute(desalins, desalouts)

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

        "wec_mass": inputs["wec_mass"],
        "inertia_matrix": inputs["inertia_matrix"],
        "Vo": inputs["w"]*inputs["t"]*inputs["draft"],
        "draft": inputs["draft"],
        "cog": inputs["cog"],

        "joint_depth": inputs["joint_depth"],
        "intake_x": inputs["intake_x"],

        "piston_area": inputs["piston_area"],
        "piston_stroke": inputs["piston_stroke"],
        "accum_volume": inputs["accum_volume"],
        "accum_P0": inputs["accum_P0"],
        "pressure_relief": desalouts["pressure_relief"],
        "throt_resist": desalouts["throt_resist"],

        "mem_resist": desalouts["mem_resist"],
        "osmotic_pressure": desalouts["osmotic_pressure"],
    }

    sysdynouts = {}
    SysDyn = sysdyn.SysDyn()
    SysDyn.setup(eng)
    SysDyn.compute(sysdynins, sysdynouts)

    econins = {
        'feedflow_cap': inputs["capacity"]/PARAMS["recovery_ratio"],
        'permflow_cap': inputs["capacity"],
        'feedflow': sysdynouts['feedflow'],
        'permflow': sysdynouts['permflow'],
    }

    econouts = {}
    Econ = econ.Econ()
    Econ.setup()
    Econ.compute(econins, econouts)
    return econouts["LCOW"]