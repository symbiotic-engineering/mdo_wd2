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
PARAMS["water_depth"] = 12.     #   [m]         depth of the water
PARAMS["forward_speed"] = 0.    #   [m/s]       forward speed of the body
PARAMS["wave_direction"] = np.array(0.) #   [deg]   direction of the waves
PARAMS["omega"] = np.linspace(0.2,3,20) #   [rad/s] wave frequencies
PARAMS["preferred_orders"] = {  #   [-]         prefered order of the datastructure entries
    'added_mass': ('water_depth', 'omega', 'radiating_dof', 'influenced_dof'),
    'radiation_damping': ('water_depth', 'omega', 'radiating_dof', 'influenced_dof'),
    'diffraction_force': ('omega', 'wave_direction', 'influenced_dof'),
    'Froude_Krylov_force': ('omega', 'wave_direction', 'influenced_dof'),
    'excitation_force': ('omega', 'wave_direction', 'influenced_dof'),
    'hydrostatic_stiffness': ('influenced_dof', 'radiating_dof'),
}

#   WEC Params
PARAMS["body_name"] = 'Flap'    #   [-]         name of the body
PARAMS["dof"] = ["Pitch"]       #   [-]         degree(s) of freedom
PARAMS["draft"] = np.array([9.0]) #   [m]         draft of the WEC
PARAMS["unit_inertia"] =  np.array([[1.85e6]])/127000   #   [kgm^2] ratio of inertia to mass
PARAMS["cg_draft_factor"] = np.array([-7/9])    #   [-] cg = cg_draft_factor*draft
''' Old WEC Thickness Params
PARAMS["nom_thickness"] = 2.0   #   [m]         nominal thickness of the WEC
PARAMS["nom_length_min"] = 8.0  #   [m]         length limit to use nominal thickness
PARAMS["small_wec_ratio"] = 0.2 #   [-]         ratio of the WEC length to thickness for small wecs'''

#   RO Params
PARAMS["feedTDS"] = 40000       #   [mg/L]      feed total dissolved solids (note mg/L = g/m^3)
PARAMS["permTDS"] = 500         #   [mg/L]      permeate total dissolved solids
PARAMS["vanthoff"] = 2.0        #   [#]         van't Hoff factor
PARAMS["M_salt"] = 58.44        #   [g/mol]     molecular weight of salt
PARAMS["RO_flux"] = 24.6/35     #   [m/day]     nominal flux for SW30HR-380 Dry
PARAMS["Aw"] = 2.57e-12         #   [m^2]       permeability coefficient
PARAMS["Bs"] = 2.30e-8          #   [m/s]       solute transport parameter
PARAMS["recovery_ratio"] = 0.515#   [-]         recovery ratio from WAVE with nominal flow and pressure, note that this is nominal, and not what will always be the recovery ratio, as flow/pressure drops, recovery ratio will drop as well

#   Mechanism Params
PARAMS["intake_x"] = np.array([4.7])        #   [m]         x-coordinate of the intake, sim with 12.
PARAMS["intake_z"] = np.array([0.])         #   [m]         z-coordinate of the intake
PARAMS["drivetrain_mass"] = np.array([50.]) #   [kg]        mass of the piston
PARAMS["max_piston_stroke"] = np.array([8.])#   [m]         maximum stroke of the piston

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
    'width' : np.array([18.]),
    'thickness' : np.array([1.0]),        
    'wec_mass' : np.array([127000.0]),

    # Mechanism Params
    'hinge2joint' : np.array([2.0]),

    # Hydraulic Params
    'piston_area' : np.array([0.26]),
    'accum_volume' : np.array([4.0]),
    'accum_P0' : np.array([3.0]),

    # Desal Params
    'capacity' : np.array([6000]),
}

# Bounds
BOUNDS = {
    'width' : (10., 24.),
    'thickness' : (1., 5.),
    'wec_mass' : (1e6, 3e6),
    'hinge2joint' : (0.1, PARAMS["draft"]),
    'piston_area' : (1e-2, 1),
    'accum_volume' : (1e-2, 5),
    'accum_P0' : (1, 7),
    'capacity' : (1000, 10000),
}