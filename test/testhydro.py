import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.hydro.hydro as hydro
import numpy as np

class TestHydro(unittest.TestCase):
    
    def setUp(self):
        # Setup Hydro instance and inputs for each test
        self.w = 18
        self.t = 1
        self.h = 10
        self.draft = 9
        self.cog = -0.7 * self.h
        self.omegas = np.linspace(0.2, 3, 10)
        self.beta = 0
        self.rho = 1025
        self.depth = np.inf
        
        # Create Hydro object and setup
        self.Hydro = hydro.Hydro()
        self.Hydro.setup(1, 10, 1)
        
        # Define hydroins for computation
        self.hydroins = {
            "width": self.w,
            "thickness": self.t,
            "height": self.h,
            "draft": self.draft,
            "center_of_gravity": self.cog,
            "omegas": self.omegas,
            "betas": np.zeros(1),
            "density": self.rho,
            "depth": np.inf
        }
        self.hydroouts = {}

    def test_added_mass(self):
        # Run the computation
        self.Hydro.compute(self.hydroins, self.hydroouts)
        
        # Retrieve the added mass from the output
        added_mass = self.hydroouts["added_mass"]
        
        # Define the expected added mass array
        expected_added_mass = np.array([[[42285163.12033962]],
                                        [[46372394.33378035]],
                                        [[58622091.55687229]],
                                        [[61515367.33341432]],
                                        [[15474074.17884097]],
                                        [[ 5189500.04198698]],
                                        [[ 6604224.4143029 ]],
                                        [[ 6825212.99486745]],
                                        [[ 8059324.40314768]],
                                        [[ 9423835.64692607]],
                                        [[17789438.35259734]]])
        
        #Use assert_allclose with a tolerance to check if the values are "close enough"
        np.testing.assert_allclose(added_mass, expected_added_mass, atol=1e-8)
        
if __name__ == '__main__':
    unittest.main()