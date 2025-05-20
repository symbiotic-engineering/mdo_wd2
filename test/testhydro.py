import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import unittest
import src.hydro.hydro as hydro
import numpy as np
import xarray as xr
from src.params import PARAMS

def generate_test_outputs():
    shape3d = (len(PARAMS["omega"]) + 1, len(PARAMS["dof"]), len(PARAMS["dof"]))
    shape2d = (len(PARAMS["dof"]), len(PARAMS["dof"]))

    return {
        "added_mass": np.random.rand(*shape3d),
        "radiation_damping": np.random.rand(*shape3d),
        "sc_re": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "sc_im": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "fk_re": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "fk_im": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "ex_re": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "ex_im": np.random.rand(len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"])),
        "inertia_matrix": np.random.rand(*shape2d),
        "hydrostatic_stiffness": np.random.rand(*shape2d),
    }


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

    def test_dict2xarray(self):
        outputs = generate_test_outputs()
        ds = hydro.dict2xarray(outputs)

        assert isinstance(ds, xr.Dataset)

        # Check coordinates
        assert np.isclose(ds.g, PARAMS["g"])
        assert np.isclose(ds.rho, PARAMS["rho"])
        assert ds.body_name == PARAMS["body_name"]
        assert np.isclose(ds.water_depth, PARAMS["water_depth"])
        assert np.isclose(ds.forward_speed, PARAMS["forward_speed"])

        # Check data variable shapes
        assert ds["added_mass"].shape == (len(PARAMS["omega"]) + 1, len(PARAMS["dof"]), len(PARAMS["dof"]))
        assert ds["diffraction_force"].shape == (len(PARAMS["omega"]) + 1, 1, len(PARAMS["dof"]))

        # Verify complex values for forces
        assert np.all(ds["diffraction_force"].values == outputs["sc_re"] + 1j * outputs["sc_im"])
        assert np.all(ds["Froude_Krylov_force"].values == outputs["fk_re"] + 1j * outputs["fk_im"])
        assert np.all(ds["excitation_force"].values == outputs["ex_re"] + 1j * outputs["ex_im"])

if __name__ == '__main__':
    unittest.main()