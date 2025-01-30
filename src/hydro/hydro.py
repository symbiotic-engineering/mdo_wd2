import capytaine as capy
import numpy as np
import xarray as xr
import openmdao.api as om

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
        "g": outputs["g"],  # Gravity
        "rho": outputs["rho"],  # Water density
        "body_name": outputs["body_name"],  # Name of the floating body
        "water_depth": outputs["water_depth"],  # Water depth
        "forward_speed": outputs["forward_speed"],  # Speed of the body
        "omega": outputs["omega"],  # Frequency values
        "wave_direction": outputs["wave_direction"],  # Wave direction values
        "radiating_dof": outputs["radiating_dof"],  # Degrees of freedom (radiating)
        "influenced_dof": outputs["influenced_dof"],  # Degrees of freedom (influenced)
        
        # Coordinates dependent on omega
        "period": ("omega", outputs["period"]),  
        "wavenumber": ("omega", outputs["wavenumber"]),  
        "wavelength": ("omega", outputs["wavelength"]), 
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
    body.add_rotation_dof(name='Pitch')
    body.keep_only_dofs(dofs='Pitch')
    print(body.mesh.nb_faces)
    return body

def solve(body,omegas,beta,rho,depth):
    solver = capy.BEMSolver()
    hydrostatics = body.compute_hydrostatics()           # solves hydrostatics problem (no waves)
    #[S,D] = capy.Delhommeau().evaluate(body.mesh, body.mesh, free_surface=0.0, water_depth=depth, wavenumber=0.0)
    # Create problems and solve
    rad_prob = [capy.RadiationProblem(body=body,omega=omega,radiating_dof='Pitch', rho=rho, water_depth=depth) for omega in omegas]     # radiation
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = [capy.DiffractionProblem(body=body, wave_direction=beta, omega=omega, rho=rho, water_depth=depth) for omega in omegas]  # diffraction
    diff_result = solver.solve_all(diff_prob,keep_details=(True))

    # Assemble dataset
    dataset = capy.assemble_dataset(rad_result + diff_result)
    return dataset

def run(w,t,h,draft,cog,omegas,beta,rho,depth):
    body = get_rectangle(w,t,h,draft,cog)
    data = solve(body,omegas,beta,rho,depth)
    return data

class Hydro(om.ExplicitComponent):
    def setup(self,ndof,nfreq,ndir):
        self.add_input('width', val=18)
        self.add_input('thickness', val=1)
        self.add_input('height', val=10)
        self.add_input('draft', val=9)
        self.add_input('center_of_gravity', val=-9)
        self.add_input('omegas', val=np.linspace(0.2,3,nfreq))
        self.add_input('betas', val=np.zeros(ndir))
        self.add_input('density', val=1025)
        self.add_input('depth', val=np.inf)
        self.add_output('g', val=9.81)
        self.add_output('rho', val=1025)
        self.add_output('body_name', val=np.ndarray(1, dtype='<U6'))
        self.add_output('water_depth', val=np.inf)
        self.add_output('forward_speed', val=0)
        self.add_output('wave_direction', val=0)
        self.add_output('omega', val=np.linspace(0.2,3,nfreq))
        self.add_output('radiating_dof',  val=np.ndarray(ndof, dtype='<U6'))
        self.add_output('influenced_dof', val=np.ndarray(ndof, dtype='<U6'))
        self.add_output('period', val=np.zeros(nfreq))
        self.add_output('wavenumber', val=np.zeros(nfreq))
        self.add_output('wavelength', val=np.zeros(nfreq))
        self.add_output('added_mass', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('radiation_damping', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('sc_re', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('sc_im', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('fk_re', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('fk_im', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('ex_re', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('ex_im', val=np.zeros((ndof,ndof,nfreq)))
        self.add_output('inertia_matrix', val=np.zeros((ndof,ndof)))
        self.add_output('hydrostatic_stiffness', val=np.zeros((ndof,ndof)))

    def compute(self, inputs, outputs):
        w = inputs['width']
        t = inputs['thickness']
        h = inputs['height']
        draft = inputs['draft']
        cog = inputs['center_of_gravity']
        omegas = inputs['omegas']
        beta = inputs['betas']
        rho = inputs['density']
        depth = inputs['depth']
        dataset = run(w,t,h,draft,cog,omegas,beta,rho,depth)
        
        # Convert to dictionary
        outputs["g"] = dataset["g"].values
        outputs["rho"] = dataset["rho"].values
        outputs["body_name"] = str(dataset["body_name"].values)
        outputs["water_depth"] = dataset['water_depth'].values
        outputs["forward_speed"] = dataset['forward_speed'].values
        outputs["wave_direction"] = dataset["wave_direction"].values
        outputs["omega"] = dataset["omega"].values
        outputs["radiating_dof"] = dataset["radiating_dof"].values
        outputs["influenced_dof"] = dataset["influenced_dof"].values
        outputs["period"] = dataset["period"].values
        outputs["wavenumber"] = dataset['wavenumber'].values
        outputs["wavelength"] = dataset['wavelength'].values

        outputs["added_mass"] = dataset['added_mass'].values
        outputs["radiation_damping"] = dataset['radiation_damping'].values
        outputs["sc_re"] = np.real(dataset['diffraction_force'].values)
        outputs["sc_im"] = np.imag(dataset['diffraction_force'].values)
        outputs["fk_re"] = np.real(dataset['Froude_Krylov_force'].values)
        outputs["fk_im"] = np.imag(dataset['Froude_Krylov_force'].values)
        outputs["ex_re"] = np.real(dataset['excitation_force'].values)
        outputs["ex_im"] = np.imag(dataset['excitation_force'].values)
        outputs["inertia_matrix"] = dataset['inertia_matrix'].values
        outputs["hydrostatic_stiffness"] = dataset["hydrostatic_stiffness"].values

        