import numpy as np
from src.params import PARAMS
import openmdao.api as om

# Osmotic Pressure Methods
def osmotic_pressure(i,c,R,T):
    pi = i*c*R*T                # [Pa]  osmotic pressure
    return pi/1e6               # [MPa] osmotic pressure

def applegate_osmotic_pressure(T,m):
    pi = 1.12*T*sum(m)        # [psi] osmotic pressure
    return pi*6894.76/1e6     # [MPa] osmotic pressure

# RO Membrane Resistance Calculation
def mem_resistance(capacity,flux,Aw):
    A = capacity/flux               # [m^2]         required RO membrane area
    RO_admittance = Aw*A            # [m^3/Pa*s]    RO admittance
    mem_resist = 1e-6/RO_admittance # [MPa*s/m^3]   membrane resistance
    return mem_resist

# Max Pressure Calculation
def max_pressure(capacity,mem_resist,dpi):
    return capacity/(24*60*60)*mem_resist+dpi # [MPa] maximum RO pressure

# Throttle Resistance Calculation
def throt_resistance(capacity,mem_resist,dpi,recovery_ratio):
    reject_ratio = 1/recovery_ratio - 1             # [-]           reject ratio
    brine_flow = reject_ratio*capacity/(24*60*60)   # [m^3/s]       brine flow
    pressure = mem_resist*capacity/(24*60*60) + dpi # [MPa]         pressure
    return pressure/brine_flow                      # [MPa*s/m^3]   throttle resistance

class DesalParams(om.ExplicitComponent):
    def setup(self):
        self.add_input('capacity', val=6000.0)      # [m^3/day] capacity of the plant

        self.add_output('mem_resist', val=60.23)    # [MPa*s/m^3] membrane resistance
        self.add_output('pressure_relief', val=6.0) # [MPa] maximum RO pressure
        self.add_output('throt_resist', val=60.23)  # [MPa*s/m^3] throttle resistance
        self.add_output('osmotic_pressure', val=3.0)# [MPa] osmotic pressure

        self.declare_partials(of = ['mem_resist','throt_resist'], wrt = '*')

    def compute(self,inputs,outputs):
        cf = PARAMS["feedTDS"]/PARAMS["M_salt"]
        cp = PARAMS["permTDS"]/PARAMS["M_salt"]
        pif = osmotic_pressure(PARAMS["vanthoff"],cf,PARAMS["R"],PARAMS["temperature"])
        pip = osmotic_pressure(PARAMS["vanthoff"],cp,PARAMS["R"],PARAMS["temperature"])
        dpi = pif - pip

        mem_resist = mem_resistance(inputs['capacity'],PARAMS["RO_flux"],PARAMS["Aw"])
        pressure_relief = max_pressure(inputs['capacity'],mem_resist,dpi)
        throt_resist = throt_resistance(inputs['capacity'],mem_resist,dpi,PARAMS["recovery_ratio"])

        outputs['mem_resist'] = mem_resist
        outputs['pressure_relief'] = pressure_relief
        outputs['throt_resist'] = throt_resist
        outputs['osmotic_pressure'] = dpi

''' def compute_partials(self,inputs,partials):
        partials['mem_resist','capacity'] = 
        partials['throt_resist','capacity'] = 
'''