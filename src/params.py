import numpy as np

PARAMS = {}

# General Params
PARAMS["g"] = np.array([9.81])                  #   [m/s^2] acceleration due to gravity
PARAMS["rho"] = np.array([1025.])               #   [kg/m^3]    density of seawater
PARAMS["days_in_year"] = np.array([365.0])      #   [days/yr]   days in a year
PARAMS["distance_to_shore"] = np.array([500.0]) #   [m]     distance from WEC to shore, also length of pipe from WEC to SWRO plant
PARAMS["R"] = np.array([8.314])                 #   [J/K*mol]   ideal gas constant
PARAMS["temperature"] = np.array([298.15])      #   [K]     temperature

#   Hydro Params
PARAMS["water_depth"] = np.array([12.])         #   [m]     depth of the water
PARAMS["forward_speed"] = np.array([0.])        #   [m/s]   forward speed of the body
PARAMS["wave_direction"] = np.array(0.)         #   [deg]   direction of the waves
PARAMS["omega"] = np.linspace(0.2,3,20)         #   [rad/s] wave frequencies
PARAMS["preferred_orders"] = {                  #   [-]     prefered order of the datastructure entries
    'added_mass': ('water_depth', 'omega', 'radiating_dof', 'influenced_dof'),
    'radiation_damping': ('water_depth', 'omega', 'radiating_dof', 'influenced_dof'),
    'diffraction_force': ('omega', 'wave_direction', 'influenced_dof'),
    'Froude_Krylov_force': ('omega', 'wave_direction', 'influenced_dof'),
    'excitation_force': ('omega', 'wave_direction', 'influenced_dof'),
    'hydrostatic_stiffness': ('influenced_dof', 'radiating_dof'),
}

#   WEC Params
PARAMS["body_name"] = 'Flap'                    #   [-]     name of the body
PARAMS["dof"] = ["Pitch"]                       #   [-]     degree(s) of freedom
PARAMS["draft"] = np.array([9.0])               #   [m]     draft of the WEC
PARAMS["unit_inertia"] =  np.array([[1.85e6]])/127000   #   [kgm^2] ratio of inertia to mass
PARAMS["cg_draft_factor"] = np.array([-7/9])    #   [-]     cg = cg_draft_factor*draft
''' Old WEC Thickness Params
PARAMS["nom_thickness"] = 2.0   #   [m]         nominal thickness of the WEC
PARAMS["nom_length_min"] = 8.0  #   [m]         length limit to use nominal thickness
PARAMS["small_wec_ratio"] = 0.2 #   [-]         ratio of the WEC length to thickness for small wecs'''
PARAMS["RM5_surf"] = 1214.0                     #   [m^2]   surface area for RM5 float
PARAMS["RM5_Cflap"] = 2529811*1.33              #   [2025USD]   cost of the RM5 flap
PARAMS["RM5_Cbase"] = 1283019*1.33              #   [2025USD]   cost of the RM5 base
PARAMS["RM5_Cpto"] = 197395*1.33                #   [2025USD]   cost of the RM5 PTO
PARAMS["RM5_Cmoor"] = 852480*1.33               #   [2025USD]   cost of the RM5 mooring
PARAMS["RM5_Cmonitoring"] = 463519*1.33         #   [2025USD/yr]    cost of the RM5 monitoring
PARAMS["RM5_CmarineOps"] = 76231*1.33           #   [2025USD/yr]    cost of the RM5 marine operations
PARAMS["RM5_CshoreOps"] = 261113*1.33           #   [2025USD/yr]    cost of the RM5 shore operations
PARAMS["RM5_Cparts"] = 64840*1.33               #   [2025USD/yr]    cost of the RM5 parts
PARAMS["RM5_Cconsumables"] = 13143*1.33         #   [2025USD/yr]    cost of the RM5 consumables

#   RO Params
PARAMS["feedTDS"] = np.array([35946])           #   [mg/L]  feed total dissolved solids (note mg/L = g/m^3)
PARAMS["permTDS"] = np.array([150])             #   [mg/L]  permeate total dissolved solids
PARAMS["vanthoff"] = np.array([2.0])            #   [#]     van't Hoff factor
PARAMS["M_salt"] = np.array([58.44])            #   [g/mol] molecular weight of salt
PARAMS["RO_flux"] = np.array([24.6/35])         #   [m/day] nominal flux for SW30HR-380 Dry
PARAMS["Aw"] = np.array([2.57e-12])             #   [m^2]   permeability coefficient
PARAMS["Bs"] = np.array([2.30e-8])              #   [m/s]   solute transport parameter
PARAMS["recovery_ratio"] = np.array([0.442])    #   [-]     recovery ratio from WAVE with nominal flow and pressure, note that this is nominal, and not what will always be the recovery ratio, as flow/pressure drops, recovery ratio will drop as well

#   Mechanism Params
PARAMS["intake_x"] = np.array([4.7])            #   [m]     x-coordinate of the intake, sim with 12.
PARAMS["intake_z"] = np.array([0.])             #   [m]     z-coordinate of the intake
PARAMS["drivetrain_mass"] = np.array([50.])     #   [kg]    mass of the driavetrain
PARAMS["rho316"] = np.array([0.29])             #   [lb/in^3]   density of 316 stainless steel
PARAMS["cost316"] = np.array([2.0])             #   [$/lb]  cost of 316 stainless steel
PARAMS["yield316"] = np.array([206e6])          #   [Pa]    yield strength of 316 stainless steel
PARAMS["modulus316"] = np.array([164e9])        #   [Pa]    modulus of elasticity of 316 stainless steel
PARAMS["fos_link"] = np.array([1.5])            #   [-]     factor of safety for the link
PARAMS["fos_cylinder"] = np.array([6])          #   [-]     factor of safety for the hydraulic cylinder
PARAMS["max_piston_stroke"] = np.array([20.])   #   [m]     maximum stroke of the piston
PARAMS["extra_stock"] = np.array([3e-3])        #   [m]     extra stock for the cylinder and cap
PARAMS["labor_factor"] = np.array([0.70])       #   [-]     labor factor for the cost of the hydraulic cylinder and rod

#   Econ Params
PARAMS["FCR"] = 0.108  # fixed charge rate
PARAMS["insurance_rate"] = 0.02  # insurance rate

# WEC-Sim Options
PARAMS["wecsimoptions"] = {
    'model' : 'src/systemdynamics/basic_wd2',
    'dt'    : 0.1,
    'tend'  : 300.0,
}

# Optimization Params
PARAMS["nworkers"] = 14

#   Dependant Params
PARAMS["period"] = 2*np.pi/PARAMS["omega"]              #   [s]     wave period
PARAMS["wavenumber"] = PARAMS["omega"]**2/PARAMS["g"]   #   [1/m]   wave number
PARAMS["wavelength"] = 2*np.pi/PARAMS["omega"]          #   [m]     wave length

# Nominal Set of Inputs
INPUTS = {
    # WEC vars
    'width' : np.array([18.]),          #   [m]     width of the WEC, sway dimension
    'thickness' : np.array([1.8]),      #   [m]     thickness of the WEC, surge dimension   
    'wec_mass' : np.array([127000.0]),  #   [kg]    mass of the WEC

    # Mechanism vars
    'hinge2joint' : np.array([1.9]),     #   [m]     distance from hinge to PTO joint

    # Hydraulic vars
    'piston_area' : np.array([0.26]),   #   [m^2]   area of the piston
    'accum_volume' : np.array([6.0]),   #   [m^3]   volume of the accumulator
    'accum_P0' : np.array([3.0]),       #   [MPa]   precharge pressure of the accumulator

    # Desal vars
    'capacity' : np.array([3100]),      #   [m^3/day]   capacity of the SWRO plant
}

# Bounds
BOUNDS = {                              #  (lower, upper) Bounds for the inputs above
    'width' : (10., 30.),
    'thickness' : (1., 5.),
    'wec_mass' : (50e3, 500e3),
    'hinge2joint' : (0.1, 4.),
    'piston_area' : (1e-1, 1),
    'accum_volume' : (1e-2, 6),
    'accum_P0' : (3, 6),
    'capacity' : (1000, 10000),
}

# Bits
BITS = {
    'width' : 8,
    'thickness' : 8,
    'wec_mass' : 8,
    'hinge2joint' : 8,
    'piston_area' : 8,
    'accum_volume' : 8,
    'accum_P0' : 8,
    'capacity' : 8,
}