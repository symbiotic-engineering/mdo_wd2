import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.desal.desal as desal
import numpy as np
from src.params import PARAMS

class TestDesal(unittest.TestCase):

    def setUp(self):
        # Create Desal object and setup
        self.Desal = desal.DesalParams()
        self.Desal.setup()

    def test_osmotic_pressure(self):
        # Test osmotic pressure
        i = PARAMS["vanthoff"]
        c = 40e3/PARAMS["M_salt"]
        R = PARAMS["R"]
        T = PARAMS["temperature"]
        pressure = desal.osmotic_pressure(i,c,R,T)
        expected_pressure = np.array([3.393318])
        np.testing.assert_allclose(pressure,expected_pressure,rtol=1e-5)
        print(f"Osmotic pressure: {pressure}")

    def test_mem_resistance(self):
        # Test membrane resistance
        capacity = 3150
        flux = PARAMS["RO_flux"]
        Aw = PARAMS["Aw"]
        resistance = desal.mem_resistance(capacity,flux,Aw)
        expected_resistance = np.array([86.820721])
        np.testing.assert_allclose(resistance,expected_resistance,rtol=1e-5)

    def test_max_pressure(self):
        # Test max pressure
        capacity = 3150
        resistance = 86.820721
        dpi = 3.39331841
        pressure = desal.max_pressure(capacity,resistance,dpi)
        expected_pressure = np.array(6.558657)
        np.testing.assert_allclose(pressure,expected_pressure,rtol=1e-5)
        print(f"Max pressure: {pressure}")

    def test_throt_resistance(self):
        # Test throttle resistance
        capacity = 3150
        resistance = 86.820721
        dpi = 3
        recovery_ratio = 0.515
        throttle = desal.throt_resistance(capacity,resistance,dpi,recovery_ratio)
        expected_throttle = np.array(179.566627)
        np.testing.assert_allclose(throttle,expected_throttle,rtol=1e-5)

    def test_full_desal(self):
        inputs = {
            "capacity": np.array([3100])
        }
        outputs = {}
        self.Desal.compute(inputs,outputs)
        expected_mem_resist = np.array([[88.221055]])
        expected_pressure_relief = np.array([[6.202019]])
        expected_throt_resist = np.array([[136.922002]])
        expected_osmotic_pressure = np.array([[3.036681]])
        np.testing.assert_allclose(outputs["mem_resist"],expected_mem_resist,rtol=1e-5)
        np.testing.assert_allclose(outputs["pressure_relief"],expected_pressure_relief,rtol=1e-5)
        np.testing.assert_allclose(outputs["throt_resist"],expected_throt_resist,rtol=1e-5)
        np.testing.assert_allclose(outputs["osmotic_pressure"],expected_osmotic_pressure,rtol=1e-5)

if __name__ == '__main__':
    unittest.main()