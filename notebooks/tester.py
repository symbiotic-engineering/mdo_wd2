import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import src.model as model
import matlab.engine
from src.params import PARAMS, INPUTS
import src.econ.WECecon as WEC

width = 18
height = 11
thickness = 1.9
print(WEC.CAPEX(width, height, thickness))
print(WEC.OPEX(width, height, thickness))