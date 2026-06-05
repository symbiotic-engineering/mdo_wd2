clear;clc;close all;
%% Load Inputs
load('data/required_matlab_variables.mat');

wecSimOptions.model = 'src/systemdynamics/basic_wd2';
wecSimOptions.tend = 300;

disp('Inputs to wdds_par:');
disp('hydro:'); disp(hydro);
disp(['wec_mass: ', num2str(wec_mass)]);
disp(['wec_inertia: ', mat2str(wec_inertia)]);
disp(['hinge_depth: ', num2str(hinge_depth)]);
disp(['joint_depth: ', num2str(joint_depth)]);
disp(['intake_x: ', num2str(intake_x)]);
disp(['intake_z: ', num2str(intake_z)]);
disp(['piston_area: ', num2str(piston_area)]);
disp(['piston_stroke: ', num2str(piston_stroke)]);
disp(['accum_volume: ', num2str(accum_volume)]);
disp(['accum_P0: ', num2str(accum_P0)]);
disp(['pressure_relief: ', num2str(pressure_relief)]);
disp(['throt_resist: ', num2str(throt_resist)]);
disp(['mem_resist: ', num2str(mem_resist)]);
disp(['osmotic_pressure: ', num2str(osmotic_pressure)]);
disp(['drivetrain_mass: ', num2str(drivetrain_mass)]);
disp(['significant_wave_height: ', num2str(significant_wave_height)]);
disp(['peak_period: ', num2str(peak_period)]);
disp(['Density of water: ', num2str(rho)]);
disp(['Gravity: ', num2str(g)]);
disp('wecSimOptions:'); disp(wecSimOptions);
disp(['key: ', num2str(key)]);

%[hydro,key] = solveIRFs_key(hydro,key);

[Qf,Qp,t,P,stroke,keyout] = wdds_sim(hydro,wec_mass,wec_inertia,...
                                hinge_depth,joint_depth,intake_x,intake_z,...
                                piston_area,piston_stroke,...
                                accum_volume,accum_P0,pressure_relief,...
                                throt_resist,mem_resist,osmotic_pressure,...
                                drivetrain_mass,...
                                significant_wave_height,peak_period,...
                                rho,g,wecSimOptions,key);

% result = wdds_par(hydro,wec_mass,wec_inertia,hinge_depth,joint_depth,intake_x,intake_z,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,osmotic_pressure,drivetrain_mass,significant_wave_height,peak_period,rho,g,wecSimOptions,key);
% [Qf,Qp,t,P,stroke,keyout] = fetchOutputs(result);
% disp(keyout)