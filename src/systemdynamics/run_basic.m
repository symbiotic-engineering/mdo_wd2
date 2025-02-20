clear;clc;close all;
%% Select Model
model = 'basic_wd2';

%% Define Parameters
% Drivetrain
drivetrain_mass = 50;   % [kg]      Effective Mass of Drivetrain (before fluid)

%  Piston
piston_area = 0.26;     % [m^2]     Piston Area
piston_stroke = 12;     % [m]       Piston Stroke Length

%  Hydraulic Smoothing
accum_volume = 4;       % [m^3]     Accumulator Volume
accum_P0 = 3;           % [MPa]     Accumulator Precharge
pressure_relief = 6;    % [MPa]     Pressure Relief

%  Membrane
mem_resist = 60.23;     % [MPa*s/m^3]   Membrane Hydraulic Resistance
osmotic_pressure = 3;   % [MPa]         Osmotic Pressure Differential

%  Brine Disposal
throt_resist = 60.23;   % [MPa*s/m^3]   Throttle Valve Hydraulic Resistance

load('/home/degoede/SEA/SEAmdo_wd2/degoede_ignore/nominal_struct.mat')
hydro = rebuildhydrostruct(nominal_hydro);
thick = 1;
hinge_depth = 8.9;
joint_depth = 7;
intake_x = 4.7;
wecSimOptions = struct();
wecSimOptions.model = model;
wecSimOptions.dt = 0.1;
wecSimOptions.tend = 300;
key=3;
wec_mass = 127000;
wec_inertia = [1.85e6 1.85e6 1.85e6];
[feed,perm,t,key] = wdds_sim(hydro,wec_mass,wec_inertia,thick,hinge_depth,joint_depth,intake_x,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,osmotic_pressure,drivetrain_mass,wecSimOptions,key);