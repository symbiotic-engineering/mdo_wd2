clear;clc;close all;
%% Define Parameters
%  Piston
piston_area = 0.26;     % [m^2]     Piston Area
piston_stroke = 12;     % [m]       Piston Stroke Length

%  Membrane
mem_resist = 60.23;     % [MPa*s/m^3]   Membrane Hydraulic Resistance
mem_pressure_min = 30;  % [bar]         Minimum Required Pressure Across Membrane
%% Run WEC-Sim
wecSim