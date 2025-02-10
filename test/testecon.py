import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.econ.econ as econ
import numpy as np

class TestEcon(unittest.TestCase):

    def setUp(self):
        # Setup econ instance and inputs for each test
        self.feedflow_cap = 6000
        self.permflow_cap = 3000
        self.feedflow_bar = 3000
        self.permflow_bar = 1500
        
        # Create econ object and setup
        self.Econ = econ.Econ()
        self.Econ.setup()
        
        # Define hydroins for computation
        self.econins = {
            "feedflow_cap": self.feedflow_cap,
            "permflow_cap": self.permflow_cap,
            "feedflow_bar": self.feedflow_bar,
            "permflow_bar": self.permflow_bar,
        }
        self.econouts = {}

    def test_LCOW(self):
        # Example test case for a function in econ
        self.Econ.compute(self.econins, self.econouts)
        LCOW = self.econouts["LCOW"]
        expected_LCOW = 1.1305986430143982
        np.testing.assert_allclose(LCOW, expected_LCOW)
        
if __name__ == '__main__':
    unittest.main()