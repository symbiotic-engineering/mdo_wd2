import numpy as np
import xarray as xr
import openmdao.api as om
from src.params import PARAMS
from src.hydro.hydro import dict2xarray
import src.GILL.src.capy2wecSim as GILL
import matlab
import random
import time as timer

class SysDyn(om.ExplicitComponent):
    def setup(self,engine):
        # Hydrodynamics
        self.add_input('added_mass', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('radiation_damping', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('sc_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('sc_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('fk_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('fk_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('ex_re', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('ex_im', val=np.zeros((1,1,len(PARAMS["omega"])+1)))
        self.add_input('hydrostatic_stiffness', val=np.zeros((1,1)))
        
        # WEC
        self.add_input('wec_mass', val=1.0)
        self.add_input('inertia_matrix', val=np.zeros((1,1)))
        self.add_input('Vo', val=0)
        self.add_input('draft', val=0)
        self.add_input('cog', val=0)
        self.add_input('thickness', val=1.0)

        # Pumping Mechanism
        self.add_input('hinge_depth', val=8.9)
        self.add_input('joint_depth', val=7.0)
        self.add_input('intake_x', val=4.7)
        self.add_input('drivetrain_mass', val=1.0)
        
        # Hydraulics
        self.add_input('piston_area', val=0.26)
        self.add_input('piston_stroke', val=4.0)
        self.add_input('accum_volume', val=4.0)
        self.add_input('accum_P0', val=3.0)
        self.add_input('pressure_relief', val=6.0)
        self.add_input('throt_resist', val=60.23)

        # RO Membrane
        self.add_input('mem_resist', val=60.23)
        self.add_input('osmotic_pressure', val=3.0)

        # MATLAB Engine
        self.eng = engine

        # Outputs
        timesteps = int(PARAMS["wecsimoptions"]["tend"]/PARAMS["wecsimoptions"]["dt"])+1
        self.add_output('feedflow', val=np.zeros(timesteps))
        self.add_output('permflow', val=np.zeros(timesteps))
        
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
        cb = np.array([0.0,0.0,0.5*inputs["draft"]])
        cg = np.array([0.0,0.0,inputs["cog"]])
        hydro = self.eng.struct()
        hydro = GILL.capy2struct(hydro, hydroXR, inputs['Vo'], cb, cg)
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

        if PARAMS["nworkers"] == 0:
            Qf,Qp,t,keyout = self.eng.wdds_sim(hydro,inputs["wec_mass"],wec_inertia,inputs["thickness"],
                                        inputs["hinge_depth"],inputs["joint_depth"],inputs["intake_x"],
                                        inputs["piston_area"],inputs["piston_stroke"],
                                        inputs["accum_volume"],inputs["accum_P0"],inputs["pressure_relief"],
                                        inputs["throt_resist"],inputs["mem_resist"],inputs["osmotic_pressure"],
                                        inputs["drivetrain_mass"],
                                        wecSimOptions,key, nargout=4)
        else:
            simouts = self.eng.wdds_par(hydro,inputs["wec_mass"],wec_inertia,inputs["thickness"],
                                        inputs["hinge_depth"],inputs["joint_depth"],inputs["intake_x"],
                                        inputs["piston_area"],inputs["piston_stroke"],
                                        inputs["accum_volume"],inputs["accum_P0"],inputs["pressure_relief"],
                                        inputs["throt_resist"],inputs["mem_resist"],inputs["osmotic_pressure"],
                                        inputs["drivetrain_mass"],
                                        wecSimOptions,key, nargout=1)
            Qf,Qp,t,keyout = self.eng.fetchOutputs(simouts,nargout=4)
        
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


