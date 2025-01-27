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
    data = hydro.run(w,t,h,draft,cog,omegas,beta,rho,depth)
    end_time = time.time()
    print(f'Total time: {end_time-start_time}')
    stopwatch.append(end_time-start_time)
print(np.mean(stopwatch))
