import numpy as np

PARAMS = {}

# General Params
PARAMS["g"] = 9.81              #   [m/s^2]     acceleration due to gravity
PARAMS["rho"] = 1025.           #   [kg/m^3]    density of seawater
PARAMS["days_in_year"] = 365.0  #   [days/yr]   days in a year
PARAMS["distance_to_shore"] = 500.0 #   [m]     distance from WEC to shore, also length of pipe from WEC to SWRO plant
PARAMS["R"] = 8.314             #   [J/K*mol]   ideal gas constant
PARAMS["temperature"] = 298.15  #   [K]         temperature

#   Hydro Params
PARAMS["body_name"] = 'Flap'    #   [-]         name of the body
PARAMS["water_depth"] = 12.     #   [m]         depth of the water
PARAMS["forward_speed"] = 0.    #   [m/s]       forward speed of the body
PARAMS["wave_direction"] = np.array(0.) #   [deg]   direction of the waves
PARAMS["omega"] = np.linspace(0.2,3,20) #   [rad/s] wave frequencies
PARAMS["dof"] = ["Pitch"]       #   [-]         degree(s) of freedom

#   RO Params
PARAMS["feedTDS"] = 40000       #   [mg/L]      feed total dissolved solids (note mg/L = g/m^3)
PARAMS["permTDS"] = 500         #   [mg/L]      permeate total dissolved solids
PARAMS["vanthoff"] = 2.0        #   [#]         van't Hoff factor
PARAMS["M_salt"] = 58.44        #   [g/mol]     molecular weight of salt
PARAMS["RO_flux"] = 24.6/35     #   [m/day]     nominal flux for SW30HR-380 Dry
PARAMS["Aw"] = 2.57e-12         #   [m^2]       permeability coefficient
PARAMS["Bs"] = 2.30e-8          #   [m/s]       solute transport parameter
PARAMS["recovery_ratio"] = 0.515#   [-]         recovery ratio from WAVE with nominal flow and pressure, note that this is nominal, and not what will always be the recovery ratio, as flow/pressure drops, recovery ratio will drop as well

#   System Dynamics Params
PARAMS["intake_x"] = 4.7        #   [m]         x-coordinate of the intake, sim with 12.
PARAMS["intake_z"] = 0.         #   [m]         z-coordinate of the intake
PARAMS["drivetrain_mass"] = 50. #   [kg]        mass of the piston
PARAMS["max_piston_stroke"] = 8.0   #   [m]     maximum stroke of the piston


#   Econ Params
PARAMS["FCR"] = 0.108  # fixed charge rate

# WEC-Sim Options
PARAMS["wecsimoptions"] = {
    'model' : 'src/systemdynamics/basic_wd2',
    'dt'    : 0.1,
    'tend'  : 300.0,
}

# Optimization Params
PARAMS["nworkers"] = 0

#   Dependant Params
PARAMS["period"] = 2*np.pi/PARAMS["omega"]  # wave period
PARAMS["wavenumber"] = PARAMS["omega"]**2/PARAMS["g"]  # wave number
PARAMS["wavelength"] = 2*np.pi/PARAMS["omega"]  # wave length

# Nominal Set of Inputs
INPUTS = {
    # WEC Params
    'w' : 18,
    't' : 1.0,
    'draft' : 9,
    'cog' : -0.7 * 10,
    'wec_mass' : 127000.0,
    'inertia_matrix' : np.array([[1.85e6]]),

    # Mechanism Params
    'joint_depth' : 7.0,

    # Hydraulic Params
    'piston_area' : 0.26,
    'accum_volume' : 4.0,
    'accum_P0' : 3.0,

    # Desal Params
    'capacity' : 6000,
}