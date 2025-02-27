import concurrent.futures
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import src.model as model
import matlab.engine
from src.params import PARAMS
from matplotlib import pyplot as plt

def run_simulation(inputs, eng):
    return model.run_sim(inputs, eng)  # Run the simulation with the shared engine

def run_simulation_in_parallel(simulation_inputs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=PARAMS["nworkers"]) as executor:
        futures = {executor.submit(run_simulation, inputs, eng): i for i, inputs in enumerate(simulation_inputs)}

        results = [None] * len(simulation_inputs)
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            results[index] = future.result()

    return results

if __name__ == "__main__":
    future_eng = matlab.engine.start_matlab(background=True)
    eng = future_eng.result()

    initialization_script_path = "/home/degoede/SEA/mdo_wd2/src/"
    eng.cd(initialization_script_path, nargout=0)
    eng.initializematlab(PARAMS["nworkers"],nargout=0)
    eng.cd('..', nargout=0)

    nominal_inputs = {
        # WEC Params
        'w' : 18,
        't' : 1.0,
        'draft' : 9,
        'cog' : -0.7 * 10,
        'wec_mass' : 127000.0,
        'inertia_matrix' : np.array([[1.85e6]]),

        # Mechanism Params
        'joint_depth' : 5.0,
        'intake_x' : 3.5,

        # Hydraulic Params
        'piston_area' : 0.26,
        'piston_stroke' : 12.0,
        'accum_volume' : 4.0,
        'accum_P0' : 3.0,

        # Desal Params
        'capacity' : 6000,
    }
    model.run_sim(nominal_inputs,eng)
    print("starting par runs...")
    simulation_inputs = [nominal_inputs]
    for intake_x in np.arange(4, 20.5, 0.5):
        simulation_inputs.append({
            **nominal_inputs,
            "intake_x": intake_x
        })
    
    results = run_simulation_in_parallel(simulation_inputs)
    
    # Plot results
    intake_x_values = [inputs['intake_x'] for inputs in simulation_inputs]
    plt.plot(intake_x_values, results, marker='o')
    plt.xlabel('intake_x')
    plt.ylabel('LCOW')
    plt.grid(True)
    plt.show()
