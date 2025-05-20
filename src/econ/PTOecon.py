import numpy as np
from src.params import PARAMS
from scipy.interpolate import Rbf
from scipy.optimize import brentq
import openmdao.api as om

def accum_cost(accum_vol):
    return 1.62124086e+05*accum_vol**9.86473502e-01

def piston_od(piston_area,piston_stroke,p_i):
    r_i = (piston_area/np.pi)**0.5
    def piston_stress(r_o):
        sigma_a = p_i*r_i**2 / (r_o**2 - r_i**2)
        sigma_c = (p_i*r_i**2) / (r_o**2 - r_i**2) + (r_i**2*r_o**2*p_i) / ((r_o**2 - r_i**2)*r_i**2)
        sigma_r = (p_i*r_i**2) / (r_o**2 - r_i**2) - (r_i**2*r_o**2*p_i) / ((r_o**2 - r_i**2)*r_i**2)
        sigma_vm = (((sigma_a - sigma_c)**2 + (sigma_c - sigma_r)**2 + (sigma_r - sigma_a)**2)/2)**0.5
        return sigma_vm
    
    def objective(r_o):
        return piston_stress(r_o)*PARAMS["factor_of_safety"] - PARAMS["yield316"]

    try:
        r_o_optimal = brentq(objective, r_i * 1.01, r_i * 10)
        return r_o_optimal*2
    except ValueError as e:
        print(f"Root finding failed: {e}")
        raise om.analysisError("Failed to find an optimal outer radius for the piston")

def piston_ASME(piston_area,piston_stroke,p_i):
    bore_m = ((piston_area/np.pi)**0.5)*2
    d = bore_m*1e3
    P = p_i
    S = PARAMS["yield316"]/PARAMS["fos_cylinder"]
    C = 0.3                             
    E = 0.8                             
    cap_t_mm = d*((C*P)/(S*E))**(1/2)
    R =  d/2
    cyl_t_mm = P*R/(S*E - 0.6*P)
    cap_t = cap_t_mm/1e3
    cyl_t = cyl_t_mm/1e3
    return cap_t, cyl_t, bore_m

def piston_cost(piston_area,piston_stroke,pi):
    cap_t, cyl_t, bore = piston_ASME(piston_area,piston_stroke,pi)
    cap_t = cap_t + PARAMS["extra_stock"]
    cyl_t = cyl_t + PARAMS["extra_stock"]
    od = bore + 2*cyl_t
    vol = piston_stroke*((od/2)**2-(bore/2)**2)*np.pi + 2*cap_t*((od/2)**2)*np.pi + cap_t*((bore/2)**2)*np.pi
    vol_in3 = vol*61023.7441
    weight = vol_in3*PARAMS["rho316"]
    mats_cost = weight*PARAMS["cost316"]
    labor_cost = PARAMS["labor_factor"]*mats_cost
    return mats_cost + labor_cost

def link_cost(l1,l2,l3,load_force):
    dz = l1-l3
    dx = l2
    length = (dz**2 + dx**2)**0.5
    link_area_load = load_force*PARAMS["fos_link"]/PARAMS["yield316"]
    required_I = load_force*PARAMS["fos_link"]*(0.699*length)**2/np.pi**2/PARAMS["modulus316"]
    required_r = (required_I*4/np.pi)**0.25
    link_area_buck = np.pi*required_r**2
    link_area = max(link_area_load,link_area_buck)
    link_r = (link_area/np.pi)**0.5
    area = np.pi*(link_r+PARAMS["extra_stock"])**2
    vol = area*length*61023.7441
    weight = vol*PARAMS["rho316"]
    mats_cost = weight*PARAMS["cost316"]
    labor_cost = PARAMS["labor_factor"]*mats_cost
    return mats_cost + labor_cost

def CAPEX(piston_area,piston_stroke,accum_vol,l1,l2,l3,pressure):
    capex = []    
    capex.append(piston_cost(piston_area,piston_stroke,pressure*1e6))
    capex.append(accum_cost(accum_vol))
    capex.append(link_cost(l1,l2,l3,pressure*piston_area*1e6))
    return sum(capex)

def OPEX(piston_area,piston_stroke,accum_vol):
    return 0