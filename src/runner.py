import numpy as np
import matlab.engine
from src.params import PARAMS, INPUTS, BOUNDS, BITS
import openmdao.api as om
from src.OpenMDAO.openmdao.drivers.robust_genetic_algorithm import RobustGADriver
import src.designvariablemapper.designvariablemapper as dvmapper
import src.hydro.hydro as hydro
import src.systemdynamics.sysdyn as sysdyn
import src.econ.econ as econ
import src.desal.desal as desal

class RunWDDS:
    def __init__(self,eng):
        self.eng = eng
        self.prob = None

    def create_problem(self):
        self.prob = om.Problem()

        self.prob.model.add_subsystem('Mapper',dvmapper.DesignVariableMapper(),promotes_inputs=["*"],promotes_outputs=["*"])
        self.prob.model.add_subsystem('Hydro',hydro.Hydro(),promotes_inputs=["*"],promotes_outputs=["*"])
        self.prob.model.add_subsystem('DesalParams',desal.DesalParams(),promotes_inputs=["*"],promotes_outputs=["*"])
        self.prob.model.add_subsystem('SysDyn',sysdyn.SysDyn(self.eng),promotes_inputs=["*"],promotes_outputs=["*"])
        self.prob.model.add_subsystem('Econ',econ.Econ(),promotes_inputs=["*"],promotes_outputs=["*"])

        for key, val in INPUTS.items():
            lower, upper = BOUNDS.get(key, (None, None))
            self.prob.model.add_design_var(key, lower=lower, upper=upper)

        self.prob.model.add_objective('LCOW')
    
    def latin_hypercube(self, num_samples):
        self.create_problem()
        self.prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=num_samples))
        self.prob.driver.options['run_parallel'] = True
        self.prob.driver.options['procs_per_model'] = 1
        recorder = om.SqliteRecorder('cases.sql')
        self.prob.driver.add_recorder(recorder)
        
        self.prob.setup()
        self.prob.run_driver()
        self.prob.cleanup()

    def solve_once(self, design_variables = INPUTS):
        self.prob.driver = om.SimpleGADriver()
        self.prob.setup()
        for var_name, var_value in design_variables.items():
            self.prob.set_val(var_name, var_value)
        self.prob.run_model()
        return self.prob.get_val('LCOW')

    def optimize(self,pop=80,generations=1e3):
        self.create_problem()
        self.prob.driver = om.SimpleGADriver()
        self.prob.setup()
        self.prob.driver.options['bits'] = BITS
        self.prob.driver.options['pop_size'] = pop
        self.prob.driver.options['max_gen'] = generations
        self.prob.driver.options['run_parallel'] = True
        self.prob.run_driver()
        return self.prob.get_val('LCOW')
    
    def robust_optimize(self,pop=80,gen_limit=1e3,patience=50,tolerence=1e-3):
        self.create_problem()
        self.prob.driver = RobustGADriver()
        self.prob.setup()
        self.prob.driver.options['bits'] = BITS
        self.prob.driver.options['pop_size'] = pop
        self.prob.driver.options['max_gen'] = gen_limit
        self.prob.driver.options['patience'] = patience
        self.prob.driver.options['tol'] = tolerence
        self.prob.driver.options['run_parallel'] = True
        self.prob.run_driver()
        return self.prob.get_val('LCOW')