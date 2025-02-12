function [] = initializematlab()
% intializes path to run WEC-Sim and source code properly
run ../src/WEC-Sim/addWecSimSource.m
addpath ../src/
addpath ../src/sea-lab-utils/plotutilities
addpath(genpath('../src/systemdynamics'))
addpath(genpath('../src/GILL/src'))
end