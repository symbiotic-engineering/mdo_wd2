import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import matlab.engine
from src.runner import RunWDDS
from src.DEAPSEA.src.ga import DeapSeaGa as GA
from src.params import PARAMS, BOUNDS, BITS
import src.econ.econ as econ
import src.econ.WECecon as WECecon
from threadpoolctl import threadpool_limits
threadpool_limits(limits=1, user_api='blas')
threadpool_limits(limits=1, user_api='openmp')


future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

initialization_script_path = parent_folder + '/src'
eng.cd(initialization_script_path, nargout=0)
eng.initializematlab(PARAMS["nworkers"],nargout=0)
eng.cd('..', nargout=0)

def hydro_energy(ind):
    Runner = RunWDDS(eng)
    out = Runner.hydro(ind)
    #print(f"Hydro output: {out}")
    period = 9.86
    omega = 2*np.pi/period
    bem_omega = PARAMS["omega"]
    f_e = np.interp(omega, bem_omega, np.ravel(out['f_e'][0:-1]))
    A = np.interp(omega, bem_omega, np.ravel(out['A'][0:-1]))
    B = np.interp(omega, bem_omega, np.ravel(out['B'][0:-1]))
    C = out['K_hs']
    I = np.ravel(out['I']) + ind['wec_mass']*(PARAMS['draft'] + out['cg'])**2
    Xidot = f_e/(-1j*(I + A)*omega + B + 1j*C/omega)
    return 1/2*(I+A)*np.abs(Xidot)**2

def hydro_objective(ind):
    mechanical_energy = hydro_energy(ind)
    CAPEX = WECecon.CAPEX(ind["width"],ind["thickness"],PARAMS["draft"])
    OPEX = WECecon.OPEX(ind["width"],ind["thickness"],PARAMS["draft"])
    LCOME = econ.LCOW(mechanical_energy, CAPEX, OPEX, PARAMS["FCR"])    # Levelized Cost of Mechanical Energy
    return (LCOME,)

def safe_hydro_objective(ind):
    try:
        return hydro_objective(ind)
    except Exception as e:
        print(f"Error in objective function: {e}")
        return (np.inf,)  # Return a large value to indicate failure

HYDRO_VARS = ["width", "thickness", "wec_mass"]
HYDRO_BOUNDS = {var: BOUNDS[var] for var in HYDRO_VARS}
HYDRO_BITS = {var: BITS[var] for var in HYDRO_VARS}

hydro_ga = GA(safe_hydro_objective, HYDRO_BOUNDS, HYDRO_BITS,
        NGEN=500, NPOP=96, NWORKERS=PARAMS["nworkers"],
        CXPB=0.8, MUTPB=0.03, ELITES_SIZE=2, TOURNAMENT_SIZE=3,
        PATIENCE=100, TOL=1e-3, csv_path="data/newresults_hydro.csv")
results = hydro_ga.run()
HYDRO_OPT = results[0]
print("Hydro optimization complete.")

HYDRO_ENERGY = hydro_energy(HYDRO_OPT)

# So rn I have a way to optimize the hydro variable for maximum mecahanical energy...
# Now I need to optimize the rest...
# one way to do this is to use the hydro energy as an input and identify a SWRO capacity that is an energy match
# another way is to find the lowest LCOCAPACITY plant
# another way is to do the above but with a constraint on max energy being the hydro energy
# i think I like this, it allows me to use the hydro energy as a constraint while still being economically based



eng.quit()
