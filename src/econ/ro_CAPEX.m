function [CAPEX] = ro_CAPEX(feedcap,capacity,pipelength,feedTDS)
% Returns the CAPEX attributed to RO plant
% INPUTS:
%   feedcap     -   [m^3/day]   Maximum feed flow (intake)
%   capacity    -   [m^3/day]   Maximum permeate flow (product)
%   pipelength  -   [m]         Length of intake pipe
%   feedTDS     -   [mg/L]      Total dissolved solids in feed
%
% OUTPUTs:
%   CAPEX       -   [$]         Capital expenses for RO system
%
% Note: This function uses data in 2018 USD (Voutchkov), adjusted to 2025 
% USD using a factor of 1.26.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                                 Intake                                  %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hdpeintake  = pipelength*0.001792e3*feedcap^0.7837; % [2018USD] CAPEX attributed to intake HDPE pipe
bandscreen  = 0.007936e3*feedcap^1.0210;            % [2018USD] CAPEX attributed to intake band screens
wedgewire   = 0.04816e3*feedcap^0.8412;             % [2018USD] CAPEX attributed to intake wedgewire screens
microscreen = 0.06158e3*feedcap^0.8466;             % [2018USD] CAPEX attributed to intake microscreens
intake      = (hdpeintake+bandscreen+wedgewire+microscreen)*1.26;   % [2025USD] Total Intake Costs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                             Pretreatment                                %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pre_upper   = 1.0289e3*feedcap^0.8127;          % [2018USD] Upper bound on pretreatment membrane
pre_lower   = 0.7656e3*feedcap^0.7904;          % [2018USD] Lower bound on pretreatment membrane
pretreat    = mean([pre_upper,pre_lower])*1.26; % [2025USD] Total Pretreatment Costs    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                           Reverse Osmosis                               %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
RO35        = 4.9006e3*capacity^0.7925;         % [2018USD] SWRO reverse osmosis costs for 35,000 mg/L TDS
RO46        = 5.0617e3*capacity^0.7779;         % [2018USD] SWRO reverse osmosis costs for 46,000 mg/L TDS
RO          = interp1([35e3,46e3],[RO35,RO46],feedTDS)*1.26;    % [2025USD] Total Reverse Osmosis Costs 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                             Post-processes                              %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stabilize   = 6.0711e3*capacity^0.6024;         % [2018USD] CAPEX attributed to lime-CO2 stabilizer
disinfect   = 0.4992e3*capacity^0.6000;         % [2018USD] CAPEX attributed to sodium hypochlorite disinfectant
postpro     = (stabilize+disinfect)*1.26;       % [2025USD] Total Post-processing Costs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                            Misc Construction                            %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
siteprep    = 20*capacity;                      % [2018USD] CAPEX attributed to site preperation
concr_dspl  = 40*capacity;                      % [2018USD] concrete disposal costs
waste_hndl  = 30*capacity;                      % [2018USD] Waste and Solids Handling
elec_instr  = 75*capacity;                      % [2018USD] Electrical and Instrumentation
aux_utils   = 25*capacity;                      % [2018USD] Aux, Service, Utilities
building    = 60*capacity;                      % [2018USD] Building
su_comm_acc = 20*capacity;                      % [2018USD] Startup, commisioning, acceptance testing
misc_constr = (siteprep+concr_dspl+waste_hndl+elec_instr+aux_utils+building+su_comm_acc)*1.26;  % [2025USD] Total Misc Construction costs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                           Engineering Services                          %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
prelimengr  = 25*capacity;                      % [2018USD] Preliminary Engineering
detailengr  = 90*capacity;                      % [2018USD] Detail Design
constrmanag = 45*capacity;                      % [2018USD] Construction Management
engineering = (prelimengr+detailengr+constrmanag)*1.26; % [2025USD] 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                            Product Development                          %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
admin       = 40*capacity;                      % [2018USD] Admin, contrating, managment
envpermit   = 45*capacity;                      % [2018USD] Environmental Permitting
legal       = 25*capacity;                      % [2018USD] Legal Services
proddev     = (admin+envpermit+legal)*1.26;     % [2025USD] Total Product Development Costs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                         %
%                                  Total                                  %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%CAPEX = intake+pretreat+RO+postpro+misc_constr+engineering+proddev;
CAPEX = intake+pretreat+RO+postpro;             % [2025USD] CAPEX
end