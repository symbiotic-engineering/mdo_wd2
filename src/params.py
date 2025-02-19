import numpy as np

PARAMS = {}

#   Hydro Params
PARAMS["g"] = 9.81    # acceleration due to gravity
PARAMS["rho"] = 1025. # density of seawater
PARAMS["body_name"] = 'Flap'  # name of the body
PARAMS["water_depth"] = 12. # depth of the water
PARAMS["forward_speed"] = 0. # forward speed of the body
PARAMS["wave_direction"] = np.array(0.) # direction of the waves
PARAMS["omega"] = np.linspace(0.2,3,10) # wave frequencies
PARAMS["dof"] = ["Pitch"]  # degree of freedom

#   RO Params
PARAMS["pipelength"] = 500  # length of the pipe
PARAMS["feedTDS"] = 40000  # feed total dissolved solids
PARAMS["days_in_year"] = 365.0  # days in a year
PARAMS["FCR"] = 0.108  # fixed charge rate

# WEC-Sim Options
PARAMS["wecsimoptions"] = {
    'model' : 'src/systemdynamics/basic_wd2',
    'dt'    : 0.1,
    'tend'  : 300.0,
}
PARAMS["nworkers"] = 0

#   Dependant Params
PARAMS["period"] = 2*np.pi/PARAMS["omega"]  # wave period
PARAMS["wavenumber"] = PARAMS["omega"]**2/PARAMS["g"]  # wave number
PARAMS["wavelength"] = 2*np.pi/PARAMS["omega"]  # wave length

