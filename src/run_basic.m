clear;clc;close all;
%% Define Parameters
%  Piston
piston_area = 0.26;     % [m^2]     Piston Area
piston_stroke = 12;     % [m]       Piston Stroke Length

%  Hydraulic Smoothing
accum_volume = 4;       % [m^3]     Accumulator Volume
pressure_relief = 60;   % [bar]     Pressure Relief

%  Membrane
mem_resist = 60.23;     % [MPa*s/m^3]   Membrane Hydraulic Resistance
mem_pressure_min = 30;  % [bar]         Minimum Required Pressure Across Membrane

%  Brine Disposal
throt_resist = 60.23;   % [MPa*s/m^3]   Throttle Valve Hydraulic Resistance


%% Run WEC-Sim
wecSim