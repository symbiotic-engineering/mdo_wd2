import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.runner import RunWDDS
from src.DEAPSEA.src.ga import DeapSeaGa as GA
from src.params import PARAMS, BOUNDS, BITS
import src.geometry.geometry as geom
import src.hydro.hydro as hydro
import src.econ.econ as econ
import src.econ.PTOecon as PTOecon
from threadpoolctl import threadpool_limits
import openmdao.api as om
threadpool_limits(limits=1, user_api='blas')
threadpool_limits(limits=1, user_api='openmp')

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

# While loading the MATLAB engine, run the hydrodynamics once since this was already optimized
HYDRO_RESULTS = {
    "width": 10.0,
    "thickness": 4.325490196078432,
    "wec_mass": 110000.0,
}

hydro_prob = om.Problem(reports=None)
hydro_prob.model.add_subsystem('Geom', geom.Geometry(), promotes_inputs=["*"], promotes_outputs=["*"])
hydro_prob.model.add_subsystem('Hydro', hydro.Hydro(), promotes_inputs=["*"], promotes_outputs=["*"])

for key, val in HYDRO_RESULTS.items():
    lower, upper = BOUNDS.get(key, (None, None))
    hydro_prob.model.add_design_var(key, lower=lower, upper=upper)

hydro_prob.driver = om.SimpleGADriver()
hydro_prob.setup()

for key, val in HYDRO_RESULTS.items():
    hydro_prob.set_val(key, val)

hydro_prob.run_model()

geom_outputs = {
    "cg": hydro_prob.get_val("cg"),
    "inertia_matrix": hydro_prob.get_val("inertia_matrix"),
    "Vo": hydro_prob.get_val("Vo"),
}

hydro_outputs = {
    "added_mass": hydro_prob.get_val("added_mass"),
    "radiation_damping": hydro_prob.get_val("radiation_damping"),
    "sc_re": hydro_prob.get_val("sc_re"),
    "sc_im": hydro_prob.get_val("sc_im"),
    "fk_re": hydro_prob.get_val("fk_re"),
    "fk_im": hydro_prob.get_val("fk_im"),
    "ex_re": hydro_prob.get_val("ex_re"),
    "ex_im": hydro_prob.get_val("ex_im"),
    "hydrostatic_stiffness": hydro_prob.get_val("hydrostatic_stiffness"),
}

# Store everything in the HYDRO_RESULTS dictionary
HYDRO_RESULTS.update(geom_outputs)
HYDRO_RESULTS.update(hydro_outputs)
HYDRO_RESULTS.pop("width")
HYDRO_RESULTS.pop("thickness")

print("Hydro results loaded.")
print("Hydro results:", HYDRO_RESULTS)

LOAD = {
    "mem_resist": 60.23,
    "osmotic_pressure": 3.39331841,
    "pressure_relief": 1e3, # set high to disable
    "throt_resist": 60.23,
}

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def pto_objective(ind):
    Runner = RunWDDS(eng)
    out = Runner.pto1(ind, HYDRO_RESULTS, LOAD)
    flow = np.mean(out['Q_p'])
    print("Flow:", flow)
    CAPEX = PTOecon.CAPEX(ind["piston_area"],out['stroke_length'],ind["accum_volume"],
                          ind["hinge2joint"],PARAMS["intake_x"],PARAMS["intake_z"],6.559)
    OPEX = PTOecon.OPEX(ind["piston_area"],out['stroke_length'],ind["accum_volume"])
    print("CAPEX:", CAPEX)
    LCOFLOW = econ.LCOW(flow, CAPEX, OPEX, PARAMS["FCR"])
    if LCOFLOW < 0:
        return(np.inf,)
    return (LCOFLOW,)

def safe_pto_objective(ind):
    try:
        return pto_objective(ind)
    except Exception as e:
        print(f"Error in objective function: {e}")
        return (np.inf,)  # Return a large value to indicate failure
    
PTO_VARS = ["hinge2joint", "piston_area", "accum_volume", "accum_P0"]
PTO_BOUNDS = {var: BOUNDS[var] for var in PTO_VARS}
PTO_BITS = {var: BITS[var] for var in PTO_VARS}
print("Starting optimization...")
pto_ga = GA(safe_pto_objective, PTO_BOUNDS, PTO_BITS,
            NGEN=400, NPOP=128, NWORKERS=PARAMS["nworkers"],
            CXPB=0.8, MUTPB=0.02, ELITES_SIZE=2, TOURNAMENT_SIZE=3,
            PATIENCE=100, TOL=1e-3, csv_path="data/newresults_pto1.csv")

results = pto_ga.run()
print("Optimization completed.")

eng.quit()
