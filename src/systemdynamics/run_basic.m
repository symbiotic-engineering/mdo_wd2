clear;clc;close all;
%% Select Model
model = 'basic_wd2';

%% Define Parameters
% Seastate
significant_wave_height = 2.64;
peak_period = 9.86;
% Drivetrain
drivetrain_mass = 50;   % [kg]      Effective Mass of Drivetrain (before fluid)

%  Piston
piston_area = 0.8588235294117647;     % [m^2]     Piston Area
piston_stroke = 20;     % [m]       Piston Stroke Length

%  Hydraulic Smoothing
accum_volume = 4.5670980392156855;       % [m^3]     Accumulator Volume
accum_P0 = 5.952941176470588;           % [MPa]     Accumulator Precharge
pressure_relief = 6.20201942;    % [MPa]     Pressure Relief

%  Membrane
mem_resist = 56.01505522;     % [MPa*s/m^3]   Membrane Hydraulic Resistance
osmotic_pressure = 3.03668065;   % [MPa]         Osmotic Pressure Differential

%  Brine Disposal
throt_resist = 86.93722295;   % [MPa*s/m^3]   Throttle Valve Hydraulic Resistance

load('/home/degoede/SEA/mdo_wd2/degoede_ignore/optimal_hydro.mat')
%hydro = rebuildHydroStruct(hydro,1,0);
thick = 1.988235294117647;
hinge_depth = 9.0;
joint_depth = 9-3.2505882352941176;
intake_x = 4.7;
wecSimOptions = struct();
wecSimOptions.model = model;
wecSimOptions.dt = 0.1;
wecSimOptions.tend = 300;
key=3;
wec_mass = 395882.35294117645;
wec_inertia = [0 5766790.18063919 0];
intake_z =0;
result = wdds_par(hydro,wec_mass,wec_inertia,...
    hinge_depth,joint_depth,intake_x,0,...
    piston_area,piston_stroke,...
    accum_volume,accum_P0,pressure_relief,...
    throt_resist,mem_resist,osmotic_pressure,...
    drivetrain_mass,...
    significant_wave_height,peak_period,...
    wecSimOptions,key);