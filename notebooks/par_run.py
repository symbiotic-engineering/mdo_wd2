import concurrent.futures
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import numpy as np
import src.model as model
import matlab.engine
from src.params import PARAMS, INPUTS
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

    model.run_sim(INPUTS,eng)
    print("starting par runs...")
    simulation_inputs = [INPUTS]
    for intake_x in np.arange(4, 20.5, 0.5):
        simulation_inputs.append({
            **INPUTS,
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
