clear;clc;close all;
%% Select Model
model = '../src/YuJenne';

%% Define Parameters
% Drivetrain
drivetrain_mass = 1;   % [kg]      Effective Mass of Drivetrain (before fluid)

%  Piston
piston_area = 0.26;     % [m^2]     Piston Area
piston_stroke = 12;     % [m]       Piston Stroke Length

%  Hydraulic Smoothing
accum_volume = 4;       % [m^3]     Accumulator Volume
pressure_relief = 56;   % [bar]     Pressure Relief

%  Membrane
mem_resist = 60.23;     % [MPa*s/m^3]   Membrane Hydraulic Resistance
mem_pressure_min = 30;  % [bar]         Minimum Required Pressure Across Membrane

%  Energy Recovery Unit
eru_resist = mem_resist/22; % [MPa*s/m^3]   ERU Hydraulic Resistance

%% Waves
wave_type = 'YuJenne';

%% Run WEC-Sim
wecSim

save('../data/validation/myVersion.mat','output','simout1')
