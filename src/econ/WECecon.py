import numpy as np
from src.params import PARAMS

def grasberger_cost(Ax,Aref,C1ref,C2ref): # EQ 19
    C1 = C1ref * (Ax/Aref)
    C2 = C2ref * (1 + np.log10(Ax/Aref))
    return C1 + C2

def CAPEX(width,height,thickness):
    C1ref = PARAMS["RM5_Cflap"] + PARAMS["RM5_Cbase"] + PARAMS["RM5_Cmoor"]
    C2ref = PARAMS["RM5_Cpto"] 
    Aref = PARAMS["RM5_surf"]
    Asurf = 2*width*height + 2*width*thickness + 2*height*thickness
    return grasberger_cost(Asurf,Aref,C1ref,C2ref)

def OPEX(width,height,thickness):
    capex = CAPEX(width,height,thickness)
    insurance = PARAMS["insurance_rate"]*capex
    C1ref = 0
    C2ref = PARAMS["RM5_Cmonitoring"] + PARAMS["RM5_CmarineOps"] + PARAMS["RM5_CshoreOps"] + PARAMS["RM5_Cparts"] + PARAMS["RM5_Cconsumables"]
    Aref = PARAMS["RM5_surf"]
    Ax = 2*width*height + 2*width*thickness + 2*height*thickness
    return grasberger_cost(Ax,Aref,C1ref,C2ref) + insurance