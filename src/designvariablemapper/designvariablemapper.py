import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS

class DesignVariableMapper(om.ExplicitComponent):

    def setup(self):
        self.add_input("width", val=18.)
        self.add_input("thickness", val=2.0)
        self.add_input("draft", val=9.0)
        self.add_input("cg_draft_factor", val=-7/9)
        self.add_input("wec_mass", val=127000.0)
        self.add_input("capacity", val=6000)
        
        self.add_output("cg", val=0.0)
        self.add_output("inertia_matrix", val=PARAMS["unit_inertia"]*127000.0)
        self.add_output("Vo", val=0.0)
        self.add_output("feedflow_cap", val=6000/PARAMS["recovery_ratio"])

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


