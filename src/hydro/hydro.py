import capytaine as capy
import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS, INPUTS

def dict2xarray(outputs):
    """
    Convert a dictionary back to an xarray.Dataset.

    Parameters:
    - outputs (dict): Dictionary containing dataset components.

    Returns:
    - xr.Dataset: Reconstructed dataset.
    """
    # Define coordinates (these are from the original xarray output)
    coords = {
        "g": PARAMS["g"],  # Gravity
        "rho": PARAMS["rho"],  # Water density
        "body_name": PARAMS["body_name"],  # Name of the floating body
        "water_depth": PARAMS["water_depth"],  # Water depth
        "forward_speed": PARAMS["forward_speed"],  # Speed of the body
        "omega": np.append(PARAMS["omega"],np.inf),  # Frequency values
        "wave_direction": [PARAMS["wave_direction"]],  # Wave direction values
        "radiating_dof": PARAMS["dof"],  # Degrees of freedom (radiating)
        "influenced_dof":PARAMS["dof"],  # Degrees of freedom (influenced)
        
        # Coordinates dependent on omega
        "period": ("omega", np.append(PARAMS["period"],0)),  
        "wavenumber": ("omega", np.append(PARAMS["wavenumber"],np.inf)),  
        "wavelength": ("omega", np.append(PARAMS["wavelength"],0)), 
    }
    
    # Define data variables (multi-dimensional arrays)
    data_vars = {
        "added_mass": (["omega", "radiating_dof", "influenced_dof"], outputs["added_mass"]),
        "radiation_damping": (["omega", "radiating_dof", "influenced_dof"], outputs["radiation_damping"]),
        "diffraction_force": (["omega", "wave_direction", "influenced_dof"], 
                              outputs["sc_re"] + 1j * outputs["sc_im"]),
        "Froude_Krylov_force": (["omega", "wave_direction", "influenced_dof"], 
                                outputs["fk_re"] + 1j * outputs["fk_im"]),
        "excitation_force": (["omega", "wave_direction", "influenced_dof"], 
                             outputs["ex_re"] + 1j * outputs["ex_im"]),
        "inertia_matrix": (["influenced_dof", "radiating_dof"], outputs["inertia_matrix"]),
        "hydrostatic_stiffness": (["influenced_dof", "radiating_dof"], outputs["hydrostatic_stiffness"]),
    }

    return xr.Dataset(data_vars, coords=coords)

def set_thickness(w,h):
    t = PARAMS["nom_thickness"]
    length = max(w,h)
    if length < PARAMS["nom_length_min"]: t = length*PARAMS["small_wec_ratio"]
    return t

def get_rectangle(w,t,h,draft,cog):
    n_surge = int(np.ceil(t*4/5))
    n_sway = int(np.ceil(w*26/30))
    n_heave = int(np.ceil(h*8/9.1))
    mesh = capy.meshes.predefined.rectangles.mesh_parallelepiped(size=(t,w,h), resolution=(n_surge,n_sway,n_heave), center=(0, 0, 0.5*h-draft),name='flap')
    lid = mesh.generate_lid(z=mesh.lowest_lid_position(omega_max=PARAMS["omega"][-1]))
    body = capy.FloatingBody(mesh,lid_mesh=lid)
    body_lidless = capy.FloatingBody(mesh)
    body.keep_immersed_part()
    body_lidless.keep_immersed_part()
    body.center_of_mass=np.array([0,0,cog])
    body_lidless.center_of_mass=np.array([0,0,cog])
    body.rotation_center = (0,0,-draft)
    body_lidless.rotation_center = (0,0,-draft)
    body.add_all_rigid_body_dofs()
    body_lidless.add_all_rigid_body_dofs()
    body.keep_only_dofs(dofs=PARAMS["dof"])
    body_lidless.keep_only_dofs(dofs=PARAMS["dof"])
    return body, body_lidless

def solve(body,body_lidless,add_inf=True):
    solver = capy.BEMSolver()
    hydrostatics = body.compute_hydrostatics()           # solves hydrostatics problem (no waves)
    #[S,D] = capy.Delhommeau().evaluate(body.mesh, body.mesh, free_surface=0.0, water_depth=depth, wavenumber=0.0)
    # Create problems and solve
    rad_prob = [capy.RadiationProblem(body=body, omega=omega, radiating_dof=rad_dof, rho=PARAMS["rho"], water_depth=PARAMS["water_depth"]) for rad_dof in PARAMS["dof"] for omega in PARAMS["omega"]]
    rad_result = solver.solve_all(rad_prob,keep_details=(True),progress_bar=False)
    diff_prob = [capy.DiffractionProblem(body=body, wave_direction=PARAMS["wave_direction"], omega=omega, rho=PARAMS["rho"], water_depth=PARAMS["water_depth"]) for omega in PARAMS["omega"]]  # diffraction
    diff_result = solver.solve_all(diff_prob,keep_details=(True),progress_bar=False)

    # Infinite Frequency Radiaiton Problem
    if add_inf:
        rad_prob_inf = [capy.RadiationProblem(body=body_lidless, omega=np.inf, radiating_dof=rad_dof, rho=PARAMS["rho"], water_depth=np.inf) for rad_dof in PARAMS["dof"]]
        rad_result_inf = solver.solve_all(rad_prob_inf,progress_bar=False)

    # Assemble dataset
    if add_inf:
        dataset = capy.assemble_dataset(rad_result + diff_result + rad_result_inf)
    else:
        dataset = capy.assemble_dataset(rad_result + diff_result)
    return dataset

def run(w,t,h,draft,cog,):
    body,body_lidless = get_rectangle(w,t,h,draft,cog)
    data = solve(body,body_lidless)
    return data

class Hydro(om.ExplicitComponent):
    def setup(self):
        self.add_input('width', val=INPUTS["width"])
        self.add_input('draft', val=PARAMS["draft"])
        self.add_input('thickness', val=INPUTS["thickness"])
        self.add_input('cg', val=PARAMS["cg_draft_factor"]*PARAMS["draft"])

        self.add_output('added_mass', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('radiation_damping', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('sc_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('sc_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('fk_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('fk_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('ex_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('ex_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_output('hydrostatic_stiffness', val=np.zeros((1,1)))
        self.declare_partials(of='*', wrt=['width', 'draft', 'thickness'])
        self.declare_partials(of='hydrostatic_stiffness', wrt=['cg'])

    def compute(self, inputs, outputs):
        w = inputs['width'].item()
        h = inputs['draft'].item() + 0.1
        t = inputs['thickness'].item()
        draft = inputs['draft'].item()
        cg = inputs['cg'].item()
        dataset = run(w,t,h,draft,cg)
        
        # Convert to dictionary
        for var_name, dims in PARAMS["preferred_orders"].items():
            dataset[var_name] = dataset[var_name].transpose(*dims)
        depth = PARAMS["water_depth"].item()
        outputs["added_mass"] = dataset['added_mass'].sel(water_depth=depth).values
        outputs["added_mass"][-1] = dataset['added_mass'].sel(water_depth=np.inf).values[-1]
        outputs["radiation_damping"] = dataset['radiation_damping'].sel(water_depth=depth).values
        outputs["radiation_damping"][-1] = dataset['radiation_damping'].sel(water_depth=np.inf).values[-1]
        outputs["sc_re"] = np.real(dataset['diffraction_force'].values)
        outputs["sc_im"] = np.imag(dataset['diffraction_force'].values)
        outputs["fk_re"] = np.real(dataset['Froude_Krylov_force'].values)
        outputs["fk_im"] = np.imag(dataset['Froude_Krylov_force'].values)
        outputs["ex_re"] = np.real(dataset['excitation_force'].values)
        outputs["ex_im"] = np.imag(dataset['excitation_force'].values)
        outputs["hydrostatic_stiffness"] = dataset["hydrostatic_stiffness"].values