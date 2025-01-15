function [OPEX] = ro_OPEX(Qf_mean,Qp_mean,pipelength,feedTDS)
% Returns the anual OPEX attributed to RO plant
% INPUTS:
%   Qf_mean     -   [m^3/day]   Mean feed flow (intake)
%   Qp_mean     -   [m^3/day]   Mean permeate flow (product)
%   pipelength  -   [m]         Length of intake pipe
%   feedTDS     -   [mg/L]      Total dissolved solids in feed
%
% OUTPUTs:
%   OPEX        -   [$/year]    Operational expenses for RO system
%
% Note: This function uses data in 2018 USD (Voutchkov), adjusted to 2025 
% USD using a factor of 1.26.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                                 Intake                                  %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hdpeintake  = pipelength*0.0136*Qf_mean^0.7804; % [2018USD] OPEX attributed to intake HDPE pipe
bandscreen  = 0.0002724e3*Qf_mean^1.0227;       % [2018USD] OPEX attributed to intake band screens
wedgewire   = 0.001959e3*Qf_mean^0.8430;        % [2018USD] OPEX attributed to intake wedgewire screens
microscreen = 0.002714e3*Qf_mean^0.8451;        % [2018USD] OPEX attributed to intake microscreens
intake      = (hdpeintake+bandscreen+wedgewire+microscreen)*1.26;   % [2025USD] Total Intake Costs
%disp(['total intake         : ',num2str(intake)])
%disp(['unit intake          : ',num2str(intake/(Qp_mean*365))])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                             Pretreatment                                %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pre_upper   = 0.04874e3*Qf_mean^0.8139;         % [2018USD] Upper bound on pretreatment membrane
pre_lower   = 0.05010e3*Qf_mean^0.7877;         % [2018USD] Lower bound on pretreatment membrane
pretreat    = mean([pre_upper,pre_lower])*1.26; % [2025USD] Total Pretreatment Costs    
%disp(['total pretreatment   : ',num2str(pretreat)])
%disp(['unit pretreatment    : ',num2str(pretreat/(365*Qp_mean))])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                           Reverse Osmosis                               %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
RO35        = 0.1969e3*Qp_mean^0.7814;          % [2018USD] SWRO reverse osmosis costs for 35,000 mg/L TDS
RO46        = 0.2098e3*Qp_mean^0.7922;          % [2018USD] SWRO reverse osmosis costs for 46,000 mg/L TDS
RO          = interp1([35e3,46e3],[RO35,RO46],feedTDS)*1.26;    % [2025USD] Total Reverse Osmosis Costs 
%disp(['total RO             : ',num2str(RO)])
%disp(['Unit RO              : ',num2str(RO/(Qp_mean*365))])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                             Post-processes                              %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stabilize   = 0.6040e3*Qp_mean^0.5993;          % [2018USD] OPEX attributed to lime-CO2 stabilizer
disinfect   = 0.01355e3*Qp_mean^0.7804;         % [2018USD] OPEX attributed to sodium hypochlorite disinfectant
postpro     = (stabilize+disinfect)*1.26;       % [2025USD] Total Post-processing Costs
%disp(['total postpro        : ',num2str(postpro)])
%disp(['unit postpro         : ',num2str(postpro/(Qp_mean*365))])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                                 Extras                                  %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
other_upper = 0.3652e3*Qp_mean^0.7517;          % [2018USD] Upper bound on other expenses, not energy
other_lower = 0.0329e3*Qp_mean^0.7819;          % [2018USD] Lower bound on other expenses, not energy
other       = mean([other_upper,other_lower]);  % [2018USD] OPEX attributed to other direct expenses, not energy
indir_upper = 0.3777e3*Qp_mean^0.7491;          % [2018USD] Upper bound on indirect expenses
indir_lower = 0.1685e3*Qp_mean^0.7491;          % [2018USD] Lower bound on indirect expenses
indirect    = mean([indir_lower,indir_upper]);  % [2018USD] OPEX attributed to indirect expenses
extras      = (other+indirect)*1.26;            % [2025USD] Total extra costs
%disp(['Extras total         : ',num2str(extras)])
%disp(['Unit Extras          : ',num2str(extras/(365*Qp_mean))])

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                                  Total                                  %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
OPEX    = intake+pretreat+RO+postpro+extras;    % [2025USD]     Total OPEX

end

