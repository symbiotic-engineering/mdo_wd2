import capytaine as capy
import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS

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
        "radiating_dof": [PARAMS["dof"]],  # Degrees of freedom (radiating)
        "influenced_dof":[PARAMS["dof"]],  # Degrees of freedom (influenced)
        
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


def get_rectangle(w,t,h,draft,cog):
    mesh = capy.meshes.predefined.rectangles.mesh_parallelepiped(size=(t,w,h), resolution=(2,12,8), center=(0, 0, 0.5*h-draft),name='flap')
    body = capy.FloatingBody(mesh)
    body.keep_immersed_part()
    body.center_of_mass=np.array([0,0,cog])
    body.rotation_center = (0,0,-draft)
    body.add_rotation_dof(name=PARAMS["dof"])
    body.keep_only_dofs(dofs=PARAMS["dof"])
    print(body.mesh.nb_faces)
    return body

def solve(body):
    solver = capy.BEMSolver()
    hydrostatics = body.compute_hydrostatics()           # solves hydrostatics problem (no waves)
    #[S,D] = capy.Delhommeau().evaluate(body.mesh, body.mesh, free_surface=0.0, water_depth=depth, wavenumber=0.0)
    # Create problems and solve
    rad_prob = [capy.RadiationProblem(body=body,omega=omega,radiating_dof=PARAMS["dof"], rho=PARAMS["rho"], water_depth=PARAMS["water_depth"]) for omega in PARAMS["omega"]]     # radiation
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = [capy.DiffractionProblem(body=body, wave_direction=PARAMS["wave_direction"], omega=omega, rho=PARAMS["rho"], water_depth=PARAMS["water_depth"]) for omega in PARAMS["omega"][:-1]]  # diffraction
    diff_result = solver.solve_all(diff_prob,keep_details=(True))

    # Infinite Frequency Radiaiton Problem
    rad_prob_inf = capy.RadiationProblem(body=body, omega=np.inf, radiating_dof=PARAMS["dof"], rho=PARAMS["rho"], water_depth=np.inf)
    rad_result_inf = solver.solve(rad_prob_inf)

    # Assemble dataset
    dataset = capy.assemble_dataset(rad_result + diff_result + [rad_result_inf])
    print(dataset)
    return dataset

def run(w,t,h,draft,cog,):
    body = get_rectangle(w,t,h,draft,cog)
    data = solve(body)
    return data

class Hydro(om.ExplicitComponent):
    def setup(self):
        self.add_input('width', val=18)
        self.add_input('thickness', val=1)
        self.add_input('height', val=10)
        self.add_input('draft', val=9)
        self.add_input('center_of_gravity', val=-9)

        self.add_output('added_mass', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('radiation_damping', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('sc_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('sc_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('fk_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('fk_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('ex_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('ex_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_output('inertia_matrix', val=np.zeros((1,1)))
        self.add_output('hydrostatic_stiffness', val=np.zeros((1,1)))

    def compute(self, inputs, outputs):
        w = inputs['width']
        t = inputs['thickness']
        h = inputs['height']
        draft = inputs['draft']
        cog = inputs['center_of_gravity']
        dataset = run(w,t,h,draft,cog)
        print(dataset["water_depth"].values)  # Check actual values
        print(PARAMS["water_depth"])          # Compare with the parameter
        # Convert to dictionary
        outputs["added_mass"] = dataset['added_mass'].sel(water_depth=PARAMS["water_depth"]).values
        outputs["added_mass"][-1] = dataset['added_mass'].sel(water_depth=np.inf).values[-1]
        outputs["radiation_damping"] = dataset['radiation_damping'].sel(water_depth=PARAMS["water_depth"]).values
        outputs["radiation_damping"][-1] = dataset['radiation_damping'].sel(water_depth=np.inf).values[-1]
        outputs["sc_re"] = np.real(dataset['diffraction_force'].values)
        outputs["sc_im"] = np.imag(dataset['diffraction_force'].values)
        outputs["fk_re"] = np.real(dataset['Froude_Krylov_force'].values)
        outputs["fk_im"] = np.imag(dataset['Froude_Krylov_force'].values)
        outputs["ex_re"] = np.real(dataset['excitation_force'].values)
        outputs["ex_im"] = np.imag(dataset['excitation_force'].values)
        outputs["inertia_matrix"] = dataset['inertia_matrix'].values
        outputs["hydrostatic_stiffness"] = dataset["hydrostatic_stiffness"].values

        