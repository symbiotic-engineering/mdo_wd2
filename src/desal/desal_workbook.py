import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
import numpy as np
from src.params import PARAMS

def osmotic_pressure(i,c,R,T):
    return i*c*R*T
c = PARAMS["feedTDS"]/PARAMS["M_salt"]  # [mol/m^3] concentration of salt
pi = osmotic_pressure(PARAMS["vanthoff"],c,PARAMS["R"],PARAMS["temperature"])  # [Pa] osmotic pressure
print(pi/1e6)

# alternatively
def applegate(T,m):
    return 1.12*T*sum(m)
m = np.array([1., 1.])*(PARAMS["feedTDS"]/PARAMS["M_salt"]/1e3)  # [mol/L] molarities
pi = applegate(PARAMS["temperature"],m)             # [psi] osmotic pressure
print(pi*6894.76/1e6)


pi = pi*6894.76/1e6                                 # [MPa] osmotic pressure

capacity = 6000                                     # [m^3/day] capacity of the plant
A = capacity/PARAMS["RO_flux"]                      # [m^2] required RO membrane area
print(A)

RO_admittance = PARAMS["Aw"]*A                      # [m^3/Pa*s] RO admittance
mem_resist = 1e-6/RO_admittance                     # [MPa*s/m^3] membrane resistance
print(mem_resist)

pressure_relief = capacity/(24*60*60)*mem_resist+pi # [MPa] pressure relief
print(pressure_relief)                              # Currently, doen't ever change...

# now for the throttle resistance, which is dependent on the recovery ratio we want...
recovery_ratio = 0.5
throt_resist = (capacity/(24*60*60)*mem_resist + pi)/(capacity/(24*60*60)*(1/recovery_ratio-1))
print(throt_resist)

trial_perm = 3000                                   # [m^3/day] trial flow
perm = trial_perm/(24*60*60)                        # [m^3/s] flow
new_recovery_ratio = perm*throt_resist/(perm*(mem_resist+throt_resist)+pi)
print(new_recovery_ratio)                           # Lower flows =  lower recovery ratios

# so now I just need to figure out recovery ratios for different flows...
# I'll do wave