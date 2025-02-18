function [] = initializematlab(nworkers)
% intializes path to run WEC-Sim and source code properly
tic
disp('Initializing MATLAB path and pool...')
run ../src/WEC-Sim/addWecSimSource.m
addpath ../src/
addpath ../src/sea-lab-utils/plotutilities
addpath(genpath('../src/systemdynamics'))
addpath(genpath('../src/GILL/src'))

if nworkers>0 
    parpool(nworkers);
end

toc
disp('MATLAB path and pool initialized.')
end