import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS
from src.hydro.hydro import dict2xarray

class SysDyn_basic(om.ExplicitComponent):
    def setup(self,engine):
        # Hydrodynamics
        self.add_input('added_mass', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('radiation_damping', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('sc_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('sc_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('fk_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('fk_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('ex_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('ex_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('inertia_matrix', val=np.zeros((1,1)))
        self.add_input('hydrostatic_stiffness', val=np.zeros((1,1)))
        
        # Hydraulics and Desal
        self.add_input('permflow_cap', val=3000.0)
        self.add_input('accum_volume', val=4.0)
        self.add_input('accum_precharge', val=30.0)
        self.add_input('throt_resist', val=0.1)
        self.add_input('piston_area', val=0.26)
        self.add_input('piston_stroke', val=4.0)

        # MATLAB Engine
        self.engine = engine

        # Outputs
        self.add_output('feedflow_bar', val=3000)
        self.add_output('permflow_bar', val=1500)
        
    def compute(self,inputs,outputs):
        hydroDct = {
            "added_mass": inputs["added_mass"],
            "radiation_damping": inputs["radiation_damping"],
            "sc_re": inputs["sc_re"],
            "sc_im": inputs["sc_im"],
            "fk_re": inputs["fk_re"],
            "fk_im": inputs["fk_im"],
            "ex_re": inputs["ex_re"],
            "ex_im": inputs["ex_im"],
            "inertia_matrix": inputs["inertia_matrix"],
            "hydrostatic_stiffness": inputs["hydrostatic_stiffness"],
        }
        hydroXR = dict2xarray(hydroDct)

        

