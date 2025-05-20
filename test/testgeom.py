import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.geometry.geometry as geom
import numpy as np
from src.params import PARAMS

class TestGeometry(unittest.TestCase):

    def setUp(self):
        # Create Mapper object and setup
        self.Geom = geom.Geometry()
        self.Geom.setup()

    def test_map(self):
        inputs = {
            "width": np.array([18]),
            "thickness": np.array([1]),
            "draft": np.array([9]),
            "cg_draft_factor": np.array([-0.7]),
            "wec_mass": np.array([1e6]),
        }
        outputs = {}
        self.Geom.compute(inputs,outputs)
        expected_outputs = {
            "cg": np.array([-9*0.7]),
            "inertia_matrix": np.array(1e6*PARAMS["unit_inertia"]),
            "Vo": np.array([18*1*9]),
        }
        for key in expected_outputs:
            np.testing.assert_allclose(outputs[key],expected_outputs[key])

if __name__ == '__main__':
    unittest.main()