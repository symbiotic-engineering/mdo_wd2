import numpy as np
from src.params import PARAMS
#from src.privateparams import PRIVATEPARAMS
from scipy.interpolate import Rbf
from scipy.optimize import brentq
import openmdao.api as om



def accum_cost(accum_vol):
    return 1.62124086e+05*accum_vol**9.86473502e-01

def piston_cost(piston_area,piston_stroke):
    points = np.array(list(PARAMS["piston_factors"].keys()))
    values = np.array(list(PARAMS["piston_factors"].values()))
    diameters, strokes = points[:, 0], points[:, 1]
    rbf_interpolator = Rbf(diameters, strokes, values, function='multiquadric')
    
    min_diameter = min(PARAMS["piston_factors"], key=lambda x: x[0])[0]*0.0254
    max_diameter = max(PARAMS["piston_factors"], key=lambda x: x[0])[0]*0.0254
    min_area = np.pi*(min_diameter/2)**2
    max_area = np.pi*(max_diameter/2)**2
    total_area = piston_area
    N = 1
    while piston_area > max_area:
        N += 1
        piston_area = total_area/N
    diameter = ((piston_area/np.pi)**0.5)*2*3.28084*12
    stroke_in = piston_stroke*3.28084*12
    query_point = (diameter, stroke_in)
    piston_factor = rbf_interpolator(*query_point)    
    return N * piston_factor * PARAMS["piston_unit"] * stroke_in/12

def piston_cost2(piston_area,piston_stroke,p_i):
    r_i = (piston_area/np.pi)**0.5
    def piston_stress(r_o):
        sigma_a = p_i*r_i / (r_o**2 - r_i**2)
        sigma_c = (p_i*r_i**2) / (r_o**2 - r_i**2) + (r_i**2*r_o**2*p_i) / ((r_o**2 - r_i**2)*r_i**2)
        sigma_r = (p_i*r_i**2) / (r_o**2 - r_i**2) - (r_i**2*r_o**2*p_i) / ((r_o**2 - r_i**2)*r_i**2)
        sigma_vm = (((sigma_a - sigma_c)**2 + (sigma_c - sigma_r)**2 + (sigma_r - sigma_a)**2)/2)**0.5
        return sigma_vm
    
    def objective(r_o):
        return piston_stress(r_o)*PARAMS["factor_of_safety"] - PARAMS["yield316"]

    try:
        r_o_optimal = brentq(objective, r_i * 1.1, r_i * 10)
        volume = np.pi * (r_o_optimal**2 - r_i**2) * piston_stroke + np.pi * r_i**2 * (r_o_optimal - r_i) * 3
        weight = volume * 61023.7441 * PARAMS["rho316"]
        return weight * PARAMS["cost316"]
    except ValueError as e:
        print(f"Root finding failed: {e}")
        raise om.analysisError("Failed to find an optimal outer radius for the piston")


def link_cost(l1,l2,l3,load_force):
    dz = l1-l3
    dx = l2
    length = (dz**2 + dx**2)**0.5
    link_area_load = load_force*PARAMS["factor_of_safety"]/PARAMS["yield316"]
    required_I = load_force*PARAMS["factor_of_safety"]*(0.699*length)**2/np.pi**2/PARAMS["modulus316"]
    required_r = (required_I*4/np.pi)**0.25
    link_area_buck = np.pi*required_r**2
    link_area = max(link_area_load,link_area_buck)
    vol = link_area*length*61023.7441
    weight = vol*PARAMS["rho316"]
    return weight*PARAMS["cost316"]

def CAPEX(piston_area,piston_stroke,accum_vol):
    capex = []    
    capex.append(piston_cost(piston_area,piston_stroke))
    capex.append(accum_cost(accum_vol))
    return sum(capex)

def OPEX(piston_area,piston_stroke,accum_vol):
    return 0