import hydro
import numpy as np
w = 18
t = 1
h = 10
draft = 9
cog = -0.7*h
omegas = np.linspace(0.2,3,10)
beta = 0
rho = 1025
depth = np.inf
Hydro = hydro.Hydro()
Hydro.setup(1,10,1)

hydroins = {"width":w,
            "thickness":t,
            "height":h,
            "draft":draft,
            "center_of_gravity":cog,
            "omegas":omegas,
            "betas":np.zeros(1),
            "density":rho,
            "depth":np.inf}
hydroouts = {}

Hydro.compute(hydroins,hydroouts)
dataset = hydro.dict2xarray(hydroouts)
print(dataset)