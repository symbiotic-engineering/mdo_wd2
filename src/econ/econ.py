import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS
import src.econ.ROecon as RO

def LCOW(awp, capex, opex, FCR):
    return (capex* FCR + opex) / (awp)

class Econ(om.ExplicitComponent):
    def setup(self):
        self.add_input('feedflow_cap', val=6000.0)
        self.add_input('permflow_cap', val=3000.0)
        self.add_input('feedflow_bar', val=3000.0)
        self.add_input('permflow_bar', val=1500.0)

        self.add_output('LCOW', val=1.0)

    def compute(self, inputs, outputs):
        feedflow_cap = inputs['feedflow_cap']
        permflow_cap = inputs['permflow_cap']
        feedflow_bar = inputs['feedflow_bar']
        permflow_bar = inputs['permflow_bar']
        capex = []
        opex = []

        # RO terms
        capex.append(RO.CAPEX(feedflow_cap,permflow_cap,PARAMS["pipelength"],PARAMS["feedTDS"]))
        opex.append(RO.OPEX(feedflow_bar,permflow_bar,PARAMS["pipelength"],PARAMS["feedTDS"]))

        # LCOW calculation        
        awp = feedflow_bar*PARAMS["days_in_year"]
        outputs['LCOW'] = LCOW(awp, sum(capex), sum(opex), PARAMS["FCR"])

