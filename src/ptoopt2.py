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

print("Hydro results loaded.")

DESAL_RESULTS = {
    "capacity": 2764.7058823529414
}

SAVED_RESULTS = {**HYDRO_RESULTS, **DESAL_RESULTS}

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def desalandpto_objective(ind):
    Runner = RunWDDS(eng)
    out = Runner.desalandpto(ind, SAVED_RESULTS)
    return out['LCOW']

def safe_desalandpto_objective(ind):
    try:
        return desalandpto_objective(ind)
    except Exception as e:
        print(f"Error in objective function: {e}")
        return (np.inf,)  # Return a large value to indicate failure
    
PTO_VARS = ["hinge2joint", "piston_area", "accum_volume", "accum_P0"]
PTO_BOUNDS = {var: BOUNDS[var] for var in PTO_VARS}
PTO_BITS = {var: BITS[var] for var in PTO_VARS}
print("Starting optimization...")
desal_ga = GA(safe_desalandpto_objective, PTO_BOUNDS, PTO_BITS,
                    NGEN=500, NPOP=128, NWORKERS=PARAMS["nworkers"],
                    CXPB=0.8, MUTPB=0.03, ELITES_SIZE=2, TOURNAMENT_SIZE=3,
                    PATIENCE=100, TOL=1e-3, csv_path="data/newresults_pto.csv")

results = desal_ga.run()
print("Optimization completed.")

eng.quit()
