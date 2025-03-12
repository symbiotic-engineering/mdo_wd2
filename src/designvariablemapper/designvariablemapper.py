import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS, INPUTS

class DesignVariableMapper(om.ExplicitComponent):

    def setup(self):
        self.add_input("width", val=INPUTS["width"])
        self.add_input("thickness", val=INPUTS["thickness"])
        self.add_input("draft", val=PARAMS["draft"])
        self.add_input("cg_draft_factor", val=PARAMS["cg_draft_factor"])
        self.add_input("wec_mass", val=INPUTS["wec_mass"])
        self.add_input("capacity", val=INPUTS["capacity"])
        
        self.add_output("cg", val=PARAMS["cg_draft_factor"]*PARAMS["draft"])
        self.add_output("inertia_matrix", val=PARAMS["unit_inertia"]*INPUTS["wec_mass"])
        self.add_output("Vo", val=INPUTS["width"]*INPUTS["thickness"]*PARAMS["draft"])
        self.add_output("feedflow_cap", val=INPUTS["capacity"]/PARAMS["recovery_ratio"])

        self.declare_partials("cg", "draft")
        self.declare_partials("inertia_matrix", "wec_mass")
        self.declare_partials("Vo", ["width", "thickness", "draft"])
        self.declare_partials("feedflow_cap", "capacity")

    def compute(self, inputs, outputs):
        outputs["cg"] = inputs["draft"]*inputs["cg_draft_factor"]
        outputs["inertia_matrix"] = inputs["wec_mass"]*PARAMS["unit_inertia"]
        outputs["Vo"] = inputs["width"]*inputs["thickness"]*inputs["draft"]
        outputs["feedflow_cap"] = inputs["capacity"]/PARAMS["recovery_ratio"]

    def compute_partials(self, inputs, partials):
        partials["cg", "draft"] = inputs["cg_draft_factor"]
        partials["inertia_matrix", "wec_mass"] = PARAMS["unit_inertia"]
        partials["Vo", "width"] = inputs["thickness"]*inputs["draft"]
        partials["Vo", "thickness"] = inputs["width"]*inputs["draft"]
        partials["Vo", "draft"] = inputs["width"]*inputs["thickness"]
        partials["feedflow_cap", "capacity"] = 1/PARAMS["recovery_ratio"]


