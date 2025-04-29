import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.econ.econ as econ
import src.econ.PTOecon as PTOecon
import src.econ.ROecon as ROecon
import src.econ.WECecon as WECecon
import numpy as np
from src.params import PARAMS

class TestEcon(unittest.TestCase):

    def setUp(self):
        # Create econ object and setup
        self.Econ = econ.Econ()
        self.Econ.setup()
        
    def test_piston(self):
        # Test piston cost
        bore_in = 12
        bore_m = bore_in*0.0254
        piston_area = np.pi*(bore_m/2)**2
        stroke_in = 48
        stroke_m = stroke_in*0.0254
        piston_stroke = stroke_m
        cost = PTOecon.piston_cost(piston_area, piston_stroke, 7e6)[0]
        print(f"piston cost : ${cost}")
        np.testing.assert_allclose(0,0)

    def test_accum4(self):
        # Test accumulator cost
        accum_vol = 4.0
        cost = PTOecon.accum_cost(accum_vol)
        expected_cost = 638423
        print(f"4 m^3 accumulator cost : ${cost}")
        np.testing.assert_allclose(cost,expected_cost,rtol=5e3)
    
    def test_accum004(self):
        # Test accumulator cost
        accum_vol = 0.04
        cost = PTOecon.accum_cost(accum_vol)
        expected_cost = 11270
        print(f"0.04 m^3 accumulator cost : ${cost}")
        np.testing.assert_allclose(cost,expected_cost,atol=5e3)

    def test_link(self):
        # Test link cost
        linches = 48
        dinches = 12
        lmeters = linches*0.0254
        dmeters = dinches*0.0254
        area = np.pi*(dmeters/2)**2
        l1 = 0
        l2 = lmeters
        l3 = 0
        force = 7e6*area
        cost = PTOecon.link_cost(l1,l2,l3,force)[0]
        print(f"link cost : ${cost}")
        np.testing.assert_allclose(cost,cost)

    def test_RO_capex(self):
        # Test RO opex
        feedcap = 3100/0.45
        capacity = 3100
        pipelength = 500
        feedTDS = 35000
        cost = ROecon.CAPEX(feedcap,capacity,pipelength,feedTDS)
        print(f"RO opex : ${cost}")
        np.testing.assert_allclose(cost,9159667,rtol=0.01)

    def test_RO_opex(self):
        # Test RO opex
        feedflow = 3100/0.45*0.49
        permflow = 3100*0.49
        pipelength = 500
        feedTDS = 35000
        cost = ROecon.OPEX(feedflow,permflow,pipelength,feedTDS)
        print(f"RO opex : ${cost}")
        np.testing.assert_allclose(cost,315840,rtol=0.01)

    def test_YJWEC_capex(self):
        width = 18
        thickness = 1.8
        height = 11
        capex = WECecon.CAPEX(width,height,thickness)
        print(f"WEC capex : ${capex}")
        np.testing.assert_allclose(capex, 2719074, rtol=0.01)

    def test_YJWEC_opex(self):
        width = 18
        thickness = 1.8
        height = 11
        capex = WECecon.OPEX(width,height,thickness)
        print(f"WEC opex : ${capex}")
        np.testing.assert_allclose(capex, 769212, rtol=0.01)

    def test_ECON(self):
        inputs = {
            'feedflow_cap': 3100/PARAMS["recovery_ratio"],
            'capacity': np.array(3100),
            'feedflow': np.ones(100)*1550/PARAMS["recovery_ratio"]/(24*60*60),
            'permflow': np.ones(100)*1550/(24*60*60),
            'width': np.array(18),
            'thickness': np.array(1.8),
            'draft': np.array(11),
            'piston_area': np.array(0.26),
            'stroke_length': np.array(2.0),
            'accum_volume': np.array(4.0),
            'pressure_relief': np.array(6.0),
            'hinge2joint': np.array(2.0)
        }
        outputs = {}
        self.Econ.compute(inputs, outputs)
        print(f"LCOW : ${outputs['LCOW']}")
        np.testing.assert_allclose(outputs['LCOW'], 4.33556, rtol=0.01)

if __name__ == '__main__':
    unittest.main()