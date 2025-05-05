import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS, INPUTS
import src.econ.ROecon as RO
import src.econ.WECecon as WEC
import src.econ.PTOecon as PTO

def LCOW(awp, capex, opex, FCR):
    return (capex* FCR + opex) / (awp)

class Econ(om.ExplicitComponent):
    def setup(self):
        self.add_input('feedflow_cap', val=INPUTS["capacity"]/PARAMS["recovery_ratio"])
        self.add_input('capacity', val=INPUTS["capacity"])
        timesteps = int(PARAMS["wecsimoptions"]["tend"]/PARAMS["wecsimoptions"]["dt"])+1
        self.add_input('feedflow', val=np.zeros(timesteps))
        self.add_input('permflow', val=np.zeros(timesteps))
        self.add_input('width', val=INPUTS["width"])
        self.add_input('thickness', val=INPUTS["thickness"])
        self.add_input('draft', val=PARAMS["draft"])
        self.add_input('piston_area', val=INPUTS["piston_area"])
        self.add_input('stroke_length', val=PARAMS["max_piston_stroke"])
        self.add_input('accum_volume', val=INPUTS["accum_volume"])
        self.add_input('pressure_relief', val=np.array(6.0)) 
        self.add_input('hinge2joint', val=INPUTS["hinge2joint"])

        self.add_output('LCOW', val=1000.0)

        self.declare_partials(of='LCOW', wrt='*')

    def compute(self, inputs, outputs):
        feedflow_cap = inputs['feedflow_cap'].item()
        capacity = inputs['capacity'].item()
        feedflow_bar = np.mean(inputs['feedflow'])*24*60*60  # average flow rate in m^3/day
        permflow_bar = np.mean(inputs['permflow'])*24*60*60  # average flow rate in m^3/day
        capex = []
        opex = []

        # WEC terms
        capex.append(WEC.CAPEX(inputs["width"],inputs["thickness"],inputs["draft"]))
        opex.append(WEC.OPEX(inputs["width"],inputs["thickness"],inputs["draft"]))

        # PTO terms
        capex.append(PTO.CAPEX(inputs["piston_area"],inputs["stroke_length"],inputs["accum_volume"],inputs["hinge2joint"],PARAMS["intake_x"],PARAMS["intake_z"],inputs["pressure_relief"]))
        opex.append(PTO.OPEX(inputs["piston_area"],inputs["stroke_length"],inputs["accum_volume"]))

        # RO terms
        capex.append(RO.CAPEX(feedflow_cap,capacity,PARAMS["distance_to_shore"],PARAMS["feedTDS"]))
        opex.append(RO.OPEX(feedflow_bar,permflow_bar,PARAMS["distance_to_shore"],PARAMS["feedTDS"]))

        # LCOW calculation        
        awp = permflow_bar*PARAMS["days_in_year"]
        outputs['LCOW'] = LCOW(awp, sum(capex), sum(opex), PARAMS["FCR"])

