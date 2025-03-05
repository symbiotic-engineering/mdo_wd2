import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS, INPUTS
from src.hydro.hydro import dict2xarray
import src.GILL.src.capy2wecSim as GILL
import matlab
import random
import time as timer
from matplotlib import pyplot as plt

class SysDyn(om.ExplicitComponent):
    def __init__(self,eng):
        super(SysDyn, self).__init__()
        # MATLAB Engine
        self.eng = eng
    
    def setup(self):
        # Hydrodynamics
        self.add_input('added_mass', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('radiation_damping', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('sc_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('sc_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('fk_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('fk_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('ex_re', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('ex_im', val=np.zeros((len(PARAMS["omega"])+1,1,1)))
        self.add_input('hydrostatic_stiffness', val=np.zeros((1,1)))
        
        # WEC
        self.add_input('wec_mass', val=INPUTS["wec_mass"])
        self.add_input('inertia_matrix', val=PARAMS["unit_inertia"]*INPUTS["wec_mass"])
        self.add_input('Vo', val=PARAMS["draft"]*INPUTS["width"]*INPUTS["thickness"])
        self.add_input('draft', val=PARAMS["draft"])
        self.add_input('cg', val=PARAMS["cg_draft_factor"]*PARAMS["draft"])

        # Pumping Mechanism
        self.add_input('hinge2joint', val=INPUTS["hinge2joint"])
        self.add_input('intake_x', val=PARAMS["intake_x"])
        
        # Hydraulics
        self.add_input('piston_area', val=INPUTS["piston_area"])
        self.add_input('max_piston_stroke', val=PARAMS["max_piston_stroke"])
        self.add_input('accum_volume', val=INPUTS["accum_volume"])
        self.add_input('accum_P0', val=INPUTS["accum_P0"])
        self.add_input('pressure_relief', val=6.0)
        self.add_input('throt_resist', val=60.23)

        # RO Membrane
        self.add_input('mem_resist', val=60.23)
        self.add_input('osmotic_pressure', val=3.0)

        # Outputs
        timesteps = int(PARAMS["wecsimoptions"]["tend"]/PARAMS["wecsimoptions"]["dt"])+1
        self.add_output('feedflow', val=np.zeros(timesteps))
        self.add_output('permflow', val=np.zeros(timesteps))
        self.add_output('stroke_length', val=PARAMS["max_piston_stroke"])
        
    def compute(self,inputs,outputs):
        hydroDct = {
            "added_mass": inputs["added_mass"],
            "radiation_damping": inputs["radiation_damping"],
            "sc_re": inputs["sc_re"],
            "sc_im": inputs["sc_im"],
            "fk_re": inputs["fk_re"],
            "fk_im": inputs["fk_im"],
            "ex_re": inputs["ex_re"],
            "ex_im": inputs["ex_im"],
            "inertia_matrix": inputs["inertia_matrix"],
            "hydrostatic_stiffness": inputs["hydrostatic_stiffness"],
        }

        # Build MATLAB hydro.struct
        hydroXR = dict2xarray(hydroDct)
        draft = inputs["draft"].item()
        cg = inputs["cg"].item()
        Vo = inputs["Vo"].item()
        hinge2joint = inputs["hinge2joint"].item()
        wec_mass = inputs["wec_mass"].item()
        intake_x = inputs["intake_x"].item()
        piston_area = inputs["piston_area"].item()
        max_piston_stroke = inputs["max_piston_stroke"].item()
        accum_volume = inputs["accum_volume"].item()
        accum_P0 = inputs["accum_P0"].item()
        pressure_relief = inputs["pressure_relief"].item()
        throt_resist = inputs["throt_resist"].item()
        mem_resist = inputs["mem_resist"].item()
        osmotic_pressure = inputs["osmotic_pressure"].item()

        cb_vec = np.array([0.0,0.0,0.5*draft])
        cg_vec = np.array([0.0,0.0,cg])
        hydro = self.eng.struct()
        hydro = GILL.capy2struct(hydro, hydroXR, Vo, cb_vec, cg_vec)
        hydro = self.eng.normalizeBEM(hydro)
        hydro = self.eng.solveIRFs(hydro)
        hydro = self.eng.rebuildhydrostruct(hydro)
        
        # Initialize an array to hold inertia values
        wec_inertia_np= np.zeros(3)
        # Map DOFs to indices
        dof_indices = {
            'Roll': 0,
            'Pitch': 1,
            'Yaw': 2
        }
        # Extract selected indices
        selected_indices = [dof_indices[dof] for dof in PARAMS["dof"]]
        # Populate the array with diagonal elements of the inertia matrix
        for idx_ii,ii in enumerate(selected_indices):
            inertia_value = inputs["inertia_matrix"][idx_ii,idx_ii]
            wec_inertia_np[ii] = inertia_value
        wec_inertia = matlab.double(wec_inertia_np)

        wecSimOptions = GILL.dict2struct(PARAMS["wecsimoptions"],self.eng)

        key = random.randint(0, 10**16 - 1)  # Generate a random 16-digit integer

        hinge_depth = matlab.double(draft)
        joint_depth = matlab.double(draft-hinge2joint)
        if PARAMS["nworkers"] == 0:
            Qf,Qp,t,P,stroke,keyout = self.eng.wdds_sim(hydro,wec_mass,wec_inertia,
                                        hinge_depth,joint_depth,intake_x,PARAMS["intake_z"],
                                        piston_area,max_piston_stroke,
                                        accum_volume,accum_P0,pressure_relief,
                                        throt_resist,mem_resist,osmotic_pressure,
                                        PARAMS["drivetrain_mass"],
                                        wecSimOptions,key, nargout=6)
        else:
            simouts = self.eng.wdds_par(hydro,wec_mass,wec_inertia,
                                        hinge_depth,joint_depth,intake_x,PARAMS["intake_z"],
                                        piston_area,max_piston_stroke,
                                        accum_volume,accum_P0,pressure_relief,
                                        throt_resist,mem_resist,osmotic_pressure,
                                        PARAMS["drivetrain_mass"],
                                        wecSimOptions,key, nargout=1)
            Qf,Qp,t,P,stroke,keyout = self.eng.fetchOutputs(simouts,nargout=6)

        try:
            if key != keyout:
                raise ValueError(f"wrong output fetched")
        except ValueError as e:
            print(f"Parallelization Error: {e}")
        
        feedflow = np.array(Qf)
        permflow = np.array(Qp)
        time = np.array(t)
        outputs['feedflow'] = feedflow
        outputs['permflow'] = permflow
        outputs['stroke_length'] = stroke


