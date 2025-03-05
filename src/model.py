import capytaine as capy
import numpy as np
import xarray as xr
import src.designvariablemapper.designvariablemapper as dvmapper
import src.hydro.hydro as hydro
import src.systemdynamics.sysdyn as sysdyn
import src.econ.econ as econ
import src.desal.desal as desal
from src.params import PARAMS

def run_sim(inputs,eng):
    mapins = {
        "width": inputs["width"],
        "thickness": inputs["thickness"],
        "draft": PARAMS["draft"],
        "cg_draft_factor": PARAMS["cg_draft_factor"],
        "wec_mass": inputs["wec_mass"],
        "capacity": inputs["capacity"],
    }
    mapouts = {}
    Mapper = dvmapper.DesignVariableMapper()
    Mapper.setup()
    Mapper.compute(mapins, mapouts)

    hydroins = {    
        'width': inputs["width"],
        'draft': PARAMS["draft"],
        'thickness': inputs["thickness"],
        'cg': mapouts["cg"],
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
        "inertia_matrix": mapouts["inertia_matrix"],
        "Vo": mapouts["Vo"],
        "draft": PARAMS["draft"],
        "cg": mapouts["cg"],

        "hinge2joint": inputs["hinge2joint"],
        "intake_x": PARAMS["intake_x"],

        "piston_area": inputs["piston_area"],
        "max_piston_stroke": PARAMS["max_piston_stroke"],
        "accum_volume": inputs["accum_volume"],
        "accum_P0": inputs["accum_P0"],
        "pressure_relief": desalouts["pressure_relief"],
        "throt_resist": desalouts["throt_resist"],

        "mem_resist": desalouts["mem_resist"],
        "osmotic_pressure": desalouts["osmotic_pressure"],
    }

    sysdynouts = {}
    SysDyn = sysdyn.SysDyn(eng)
    SysDyn.setup()
    SysDyn.compute(sysdynins, sysdynouts)
    print(sysdynouts["stroke_length"])
    econins = {
        'feedflow_cap': inputs["capacity"]/PARAMS["recovery_ratio"],
        'capacity': inputs["capacity"],
        'feedflow': sysdynouts['feedflow'],
        'permflow': sysdynouts['permflow'],
    }

    econouts = {}
    Econ = econ.Econ()
    Econ.setup()
    Econ.compute(econins, econouts)
    return econouts["LCOW"]