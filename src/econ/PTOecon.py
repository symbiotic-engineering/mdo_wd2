import numpy as np
from src.params import PARAMS

def accum_cost_fcn(count2,count5,count10,count15):
    return PARAMS["accum_cost_2.5G"]*count2 + PARAMS["accum_cost_5G"]*count5 + PARAMS["accum_cost_10G"]*count10 + PARAMS["accum_cost_15G"]*count15

def accum_vol_fcn(count2,count5,count10,count15):
    return 2.5*count2 + 5*count5 + 10*count10 + 15*count15

def CAPEX(piston_area,piston_stroke,accum_vol):
    capex = []
    
    # Hydraulic Cylinder cost
    piston_unit = 200

    # Accumulator Volume to Purchase
    accum_vol_gal = accum_vol * 264.172
    accum_vol_remaining = np.ceil(accum_vol_gal / 2.5)*2.5
    
    '''best_cost = float('inf')
    best_distribution = None

    # Iterate over possible counts of 15G accumulators
    for count15 in range(int(accum_vol_rounded // 15) + 1):
        # Iterate over possible counts of 10G accumulators
        for count10 in range(int((accum_vol_rounded - 15 * count15) // 10) + 1):
            # Iterate over possible counts of 5G accumulators
            for count5 in range(int((accum_vol_rounded - 15 * count15 - 10 * count10) // 5) + 1):
                # Calculate the count of 2.5G accumulators needed
                count2 = (accum_vol_rounded - 15 * count15 - 10 * count10 - 5 * count5) / 2.5
                # Check if the count of 2.5G accumulators is an integer
                if count2.is_integer():
                    count2 = int(count2)
                    # Calculate the total cost for the current distribution
                    cost = accum_cost(count2, count5, count10, count15)
                    # Update the best cost and distribution if the current cost is lower
                    if cost < best_cost:
                        best_cost = cost
                        best_distribution = (count2, count5, count10, count15)

    # Print the optimal distribution and minimum cost if found
    if best_distribution:
        count2, count5, count10, count15 = best_distribution
        print(f"Optimal distribution: 2.5G: {count2}, 5G: {count5}, 10G: {count10}, 15G: {count15}")
        print(f"Minimum cost: {best_cost}")
    else:
        print("No valid distribution found")
    capex.append(best_cost)'''
    
    # Split accumulator cost into different sizes and calculate total cost
    count15 = accum_vol_remaining// 15
    accum_vol_remaining -= count15*15
    count10 = accum_vol_remaining // 10
    accum_vol_remaining -= count10*10
    count5 = accum_vol_remaining // 5
    accum_vol_remaining -= count5*5
    count2 = accum_vol_remaining / 2.5
    accum_cost = accum_cost_fcn(count2,count5,count10,count15)
    capex.append(accum_cost)
    
    return sum(capex)

def OPEX(piston_area,piston_stroke,accum_vol):
    return 0