import hydro
import numpy as np
import time
w = 18
t = 1
h = 10
draft = 9
cog = -0.7*h
omegas = np.linspace(0.2,3,10)
beta = 0
rho = 1025
depth = np.inf
stopwatch = []
for ii in range(1):
    start_time = time.time()
    dataset = hydro.run(w,t,h,draft,cog,omegas,beta,rho,depth)
    end_time = time.time()
    print(f'Total time: {end_time-start_time}')
    stopwatch.append(end_time-start_time)
print(dataset)
outputs = {}
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

dataset = hydro.dict2xarray(outputs)
print(dataset)