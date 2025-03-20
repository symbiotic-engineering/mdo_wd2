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
        self.w = np.array([18])
        self.t = np.array([1])
        self.h = np.array([10])
        self.draft = np.array([9])
        self.cg = -0.7 * self.h
        
        # Create Hydro object and setup
        self.Hydro = hydro.Hydro()
        self.Hydro.setup()
        
        # Define hydroins for computation
        self.hydroins = {
            "width": self.w,
            "thickness": self.t,
            "height": self.h,
            "draft": self.draft,
            "cg": self.cg,
        }
        self.hydroouts = {}

    def test_added_mass(self):
        # Run the computation
        self.Hydro.compute(self.hydroins, self.hydroouts)
        #print(self.hydroouts)
        # Retrieve the added mass from the output
        added_mass_inf = self.hydroouts["added_mass"][-1]
        
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
        expected_added_mass_inf = expected_added_mass[-1]
        #Use assert_allclose with a tolerance to check if the values are "close enough"
        np.testing.assert_allclose(added_mass_inf, expected_added_mass_inf, rtol=1e-2)
        
if __name__ == '__main__':
    unittest.main()