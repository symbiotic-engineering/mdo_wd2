import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.designvariablemapper.designvariablemapper as map
import numpy as np
from src.params import PARAMS

class TestEcon(unittest.TestCase):

    def setUp(self):
        # Create Mapper object and setup
        self.Mapper = map.DesignVariableMapper()
        self.Mapper.setup()

    def test_map(self):
        inputs = {
            "width": np.array([18]),
            "thickness": np.array([1]),
            "draft": np.array([9]),
            "cg_draft_factor": np.array([-0.7]),
            "wec_mass": np.array([1e6]),
            "capacity": np.array([3150])
        }
        outputs = {}
        self.Mapper.compute(inputs,outputs)
        expected_outputs = {
            "cg": np.array([-9*0.7]),
            "inertia_matrix": np.array(1e6*PARAMS["unit_inertia"]),
            "Vo": np.array([18*1*9]),
            "feedflow_cap": np.array(3150/PARAMS["recovery_ratio"])
        }
        for key in expected_outputs:
            np.testing.assert_allclose(outputs[key],expected_outputs[key])

if __name__ == '__main__':
    unittest.main()