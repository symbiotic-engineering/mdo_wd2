function [] = initializematlab(nworkers)
% intializes path to run WEC-Sim and source code properly
disp('Initializing MATLAB path...')
run ../src/WEC-Sim/addWecSimSource.m
addpath ../src/
addpath ../src/sea-lab-utils/plotutilities
addpath(genpath('../src/systemdynamics'))
addpath(genpath('../src/GILL/src'))
disp('MATLAB path initialized.')

if nworkers>0 
    disp(['Starting parallel pool with ', num2str(nworkers), ' workers...'])
    c = parcluster('local');
    parpool(c, nworkers);
    disp('Parallel pool started.')
end

end