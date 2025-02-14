function [] = initializematlab()
% intializes path to run WEC-Sim and source code properly
tic
disp('Initializing MATLAB path...')
run ../src/WEC-Sim/addWecSimSource.m
addpath ../src/
addpath ../src/sea-lab-utils/plotutilities
addpath(genpath('../src/systemdynamics'))
addpath(genpath('../src/GILL/src'))
toc
disp('MATLAB path initialized.')
end