import numpy as np

def ro_CAPEX(feedcap, capacity, pipelength, feedTDS):
    """
    Returns the CAPEX attributed to RO plant
    INPUTS:
        feedcap     -   [m^3/day]   Maximum feed flow (intake)
        capacity    -   [m^3/day]   Maximum permeate flow (product)
        pipelength  -   [m]         Length of intake pipe
        feedTDS     -   [mg/L]      Total dissolved solids in feed

    OUTPUTs:
        CAPEX       -   [$]         Capital expenses for RO system

    Note: This function uses data in 2018 USD (Voutchkov), adjusted to 2025 
    USD using a factor of 1.26.
    """

    ###########################################################################
    #                                                                         #
    #                                 Intake                                  #
    #                                                                         #
    ###########################################################################
    hdpeintake = pipelength * 0.001792e3 * feedcap ** 0.7837  # [2018USD] CAPEX attributed to intake HDPE pipe
    bandscreen = 0.007936e3 * feedcap ** 1.0210               # [2018USD] CAPEX attributed to intake band screens
    wedgewire = 0.04816e3 * feedcap ** 0.8412                 # [2018USD] CAPEX attributed to intake wedgewire screens
    microscreen = 0.06158e3 * feedcap ** 0.8466               # [2018USD] CAPEX attributed to intake microscreens
    intake = (hdpeintake + bandscreen + wedgewire + microscreen) * 1.26  # [2025USD] Total Intake Costs

    ###########################################################################
    #                                                                         #
    #                             Pretreatment                                #
    #                                                                         #
    ###########################################################################
    pre_upper = 1.0289e3 * feedcap ** 0.8127          # [2018USD] Upper bound on pretreatment membrane
    pre_lower = 0.7656e3 * feedcap ** 0.7904          # [2018USD] Lower bound on pretreatment membrane
    pretreat = np.mean([pre_upper, pre_lower]) * 1.26 # [2025USD] Total Pretreatment Costs    

    ###########################################################################
    #                                                                         #
    #                           Reverse Osmosis                               #
    #                                                                         #
    ###########################################################################
    RO35 = 4.9006e3 * capacity ** 0.7925              # [2018USD] SWRO reverse osmosis costs for 35,000 mg/L TDS
    RO46 = 5.0617e3 * capacity ** 0.7779              # [2018USD] SWRO reverse osmosis costs for 46,000 mg/L TDS
    RO = np.interp(feedTDS, [35e3, 46e3], [RO35, RO46]) * 1.26  # [2025USD] Total Reverse Osmosis Costs 

    ###########################################################################
    #                                                                         #
    #                             Post-processes                              #
    #                                                                         #
    ###########################################################################
    stabilize = 3.2145e3 * capacity ** 0.6026         # [2018USD] CAPEX attributed to calcite-CO2 stabilizer
    # stabilize = 6.0711e3 * capacity ** 0.6024       # [2018USD] CAPEX attributed to lime-CO2 stabilizer
    disinfect = 0.4992e3 * capacity ** 0.6000         # [2018USD] CAPEX attributed to sodium hypochlorite disinfectant
    postpro = (stabilize + disinfect) * 1.26          # [2025USD] Total Post-processing Costs

    ###########################################################################
    #                                                                         #
    #                            Misc Construction                            #
    #                                                                         #
    ###########################################################################
    siteprep = 20 * capacity                          # [2018USD] CAPEX attributed to site preparation
    concr_dspl = 40 * capacity                        # [2018USD] concrete disposal costs
    waste_hndl = 30 * capacity                        # [2018USD] Waste and Solids Handling
    elec_instr = 75 * capacity                        # [2018USD] Electrical and Instrumentation
    aux_utils = 25 * capacity                         # [2018USD] Aux, Service, Utilities
    building = 60 * capacity                          # [2018USD] Building
    su_comm_acc = 20 * capacity                       # [2018USD] Startup, commissioning, acceptance testing
    misc_constr = (siteprep + concr_dspl + waste_hndl + elec_instr + aux_utils + building + su_comm_acc) * 1.26  # [2025USD] Total Misc Construction costs

    ###########################################################################
    #                                                                         #
    #                           Engineering Services                          #
    #                                                                         #
    ###########################################################################
    prelimengr = 25 * capacity                        # [2018USD] Preliminary Engineering
    detailengr = 90 * capacity                        # [2018USD] Detail Design
    constrmanag = 45 * capacity                       # [2018USD] Construction Management
    engineering = (prelimengr + detailengr + constrmanag) * 1.26  # [2025USD] 

    ###########################################################################
    #                                                                         #
    #                            Product Development                          #
    #                                                                         #
    ###########################################################################
    admin = 40 * capacity                             # [2018USD] Admin, contracting, management
    envpermit = 45 * capacity                         # [2018USD] Environmental Permitting
    legal = 25 * capacity                             # [2018USD] Legal Services
    proddev = (admin + envpermit + legal) * 1.26      # [2025USD] Total Product Development Costs

    ###########################################################################
    #                                                                         #
    #                                  Total                                  #
    #                                                                         #
    ###########################################################################
    CAPEX = intake + pretreat + RO + postpro + misc_constr + engineering + proddev
    # CAPEX = intake + pretreat + RO + postpro  # [2025USD] CAPEX
    return CAPEX

def ro_OPEX(Qf_mean, Qp_mean, pipelength, feedTDS):
    """
    Returns the annual OPEX attributed to RO plant
    INPUTS:
        Qf_mean     -   [m^3/day]   Mean feed flow (intake)
        Qp_mean     -   [m^3/day]   Mean permeate flow (product)
        pipelength  -   [m]         Length of intake pipe
        feedTDS     -   [mg/L]      Total dissolved solids in feed

    OUTPUTs:
        OPEX        -   [$/year]    Operational expenses for RO system

    Note: This function uses data in 2018 USD (Voutchkov), adjusted to 2025 
    USD using a factor of 1.26.
    """

    ###########################################################################
    #                                                                         #
    #                                 Intake                                  #
    #                                                                         #
    ###########################################################################
    hdpeintake = pipelength * 0.0136 * Qf_mean ** 0.7804  # [2018USD] OPEX attributed to intake HDPE pipe
    bandscreen = 0.0002724e3 * Qf_mean ** 1.0227          # [2018USD] OPEX attributed to intake band screens
    wedgewire = 0.001959e3 * Qf_mean ** 0.8430            # [2018USD] OPEX attributed to intake wedgewire screens
    microscreen = 0.002714e3 * Qf_mean ** 0.8451          # [2018USD] OPEX attributed to intake microscreens
    intake = (hdpeintake + bandscreen + wedgewire + microscreen) * 1.26  # [2025USD] Total Intake Costs

    ###########################################################################
    #                                                                         #
    #                             Pretreatment                                #
    #                                                                         #
    ###########################################################################
    pre_upper = 0.04874e3 * Qf_mean ** 0.8139             # [2018USD] Upper bound on pretreatment membrane
    pre_lower = 0.05010e3 * Qf_mean ** 0.7877             # [2018USD] Lower bound on pretreatment membrane
    pretreat = np.mean([pre_upper, pre_lower]) * 1.26     # [2025USD] Total Pretreatment Costs    

    ###########################################################################
    #                                                                         #
    #                           Reverse Osmosis                               #
    #                                                                         #
    ###########################################################################
    RO35 = 0.1969e3 * Qp_mean ** 0.7814                   # [2018USD] SWRO reverse osmosis costs for 35,000 mg/L TDS
    RO46 = 0.2098e3 * Qp_mean ** 0.7922                   # [2018USD] SWRO reverse osmosis costs for 46,000 mg/L TDS
    RO = np.interp(feedTDS, [35e3, 46e3], [RO35, RO46]) * 1.26  # [2025USD] Total Reverse Osmosis Costs 

    ###########################################################################
    #                                                                         #
    #                             Post-processes                              #
    #                                                                         #
    ###########################################################################
    stabilize = 0.3411e3 * Qp_mean ** 0.5996              # [2018USD] OPEX attributed to calcite-CO2 stabilizer
    #stabilize   = 0.6040e3*Qp_mean^0.5993;                # [2018USD] OPEX attributed to lime-CO2 stabilizer
    disinfect = 0.01355e3 * Qp_mean ** 0.7804             # [2018USD] OPEX attributed to sodium hypochlorite disinfectant
    postpro = (stabilize + disinfect) * 1.26              # [2025USD] Total Post-processing Costs

    ###########################################################################
    #                                                                         #
    #                                 Extras                                  #
    #                                                                         #
    ###########################################################################
    other_upper = 0.3652e3 * Qp_mean ** 0.7517            # [2018USD] Upper bound on other expenses, not energy
    other_lower = 0.0329e3 * Qp_mean ** 0.7819            # [2018USD] Lower bound on other expenses, not energy
    other = np.mean([other_upper, other_lower])           # [2018USD] OPEX attributed to other direct expenses, not energy
    indir_upper = 0.3777e3 * Qp_mean ** 0.7491            # [2018USD] Upper bound on indirect expenses
    indir_lower = 0.1685e3 * Qp_mean ** 0.7491            # [2018USD] Lower bound on indirect expenses
    indirect = np.mean([indir_lower, indir_upper])        # [2018USD] OPEX attributed to indirect expenses
    extras = (other + indirect) * 1.26                    # [2025USD] Total extra costs

    ###########################################################################
    #                                                                         #
    #                                  Total                                  #
    #                                                                         #
    ###########################################################################
    OPEX = intake + pretreat + RO + postpro + extras      # [2025USD] Total OPEX
    return OPEX