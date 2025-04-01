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
        piston_area = 0.028502296
        piston_stroke = 2
        cost = PTOecon.piston_cost(piston_area, piston_stroke)
        print(f"piston cost : ${cost}")
        np.testing.assert_allclose(0,0)

    def test_piston2(self):
        # Test piston cost
        piston_area = 0.028502296
        piston_stroke = 2
        cost = PTOecon.piston_cost2(piston_area, piston_stroke,63e6)
        print(f"piston2 cost : ${cost}")
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
        linches = 96
        dinches = 24
        lmeters = linches*0.0254
        dmeters = dinches*0.0254
        area = np.pi*(dmeters/2)**2
        l1 = 0
        l2 = lmeters
        l3 = 0
        force = 6e6*area
        cost = PTOecon.link_cost(l1,l2,l3,force)
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

if __name__ == '__main__':
    unittest.main()