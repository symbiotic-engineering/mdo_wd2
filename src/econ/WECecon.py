import numpy as np
from src.params import PARAMS

def grasberger_cost(Asurf,Abase,C1base,C2base): # EQ 19
    C1 = C1base * (Asurf/Abase)
    C2 = C2base * (1 + np.log10(Asurf/Abase))
    return C1 + C2

def CAPEX(width,height,thickness):
    C1base = PARAMS["RM5_Cflap"]
    C2base = PARAMS["RM5_Cbase"] + PARAMS["RM5_Cbear"] + PARAMS["RM5_Cmoor"]
    Abase = PARAMS["RM5_surf"]
    Asurf = 2*width*height + 2*width*thickness + 2*height*thickness
    return grasberger_cost(Asurf,Abase,C1base,C2base)

def OPEX(width,height,thickness):
    capex = CAPEX(width,height,thickness)
    insurance = PARAMS["insurance_rate"]*capex
    C1base = 0
    C2base = PARAMS["RM5_Cmonitoring"] + PARAMS["RM5_CmarineOps"] + PARAMS["RM5_CshoreOps"] + PARAMS["RM5_Cparts"] + PARAMS["RM5_Cconsumables"]
    Abase = PARAMS["RM5_surf"]
    Asurf = 2*width*height + 2*width*thickness + 2*height*thickness
    return grasberger_cost(Asurf,Abase,C1base,C2base) + insurance