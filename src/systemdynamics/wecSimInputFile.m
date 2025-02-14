%% Simulation Data
simu = simulationClass();               % Initialize Simulation Class
simu.simMechanicsFile = [model '.slx'];    % Specify Simulink Model File
%simu.mode = 'normal';                   % Specify Simulation Mode ('normal','accelerator','rapid-accelerator')
simu.explorer = 'off';                  % Turn SimMechanics Explorer (on/off)
simu.startTime = 0;                     % Simulation Start Time [s]
simu.rampTime = 0;                    % Wave Ramp Time [s]
simu.endTime = 300;                     % Simulation End Time [s]        
simu.solver = 'ode4';                   % simu.solver = 'ode4' for fixed step & simu.solver = 'ode45' for variable step - that's what WEC-Sim thinks...
simu.dt = 0.1;                          % Simulation Time-Step [s]
simu.cicEndTime = 30;                   % Specify CI Time [s]
simu.saveWorkspace = 0;                 % I don't want WEC-Sim to save my workspace for me, I can do it myself
simu.outputDir = '../../data/lastrun';

if wave_type == 'YuJenne'
    simu.startTime = 0;                     % Simulation Start Time [s]
    simu.rampTime = 100;                    % Wave Ramp Time [s]
    simu.endTime = 3000;                    % Simulation End Time [s]
    simu.dt = 0.1;                          % Simulation Time-Step [s]
    simu.cicEndTime = 30;                   % Specify CI Time [s]
end

%% Wave Information
% % noWaveCIC, no waves with radiation CIC  
% waves = waveClass('noWaveCIC');       % Initialize Wave Class and Specify Type  

% % Regular Waves 
% waves = waveClass('regular');           % Initialize Wave Class and Specify Type                                 
% waves.height = 2.5;                     % Wave Height [m]
% waves.period = 8;                       % Wave Period [s]
% Irregular Waves using PM Spectrum with Directionality 
switch wave_type
    case 'YuJenne'
        waves = waveClass('irregular');         % Initialize Wave Class and Specify Type
        waves.height = 2.64;                     % Significant Wave Height [m]
        waves.period = 9.86;                       % Peak Period [s]
        waves.spectrumType = 'PM';              % Specify Spectrum Type
        waves.bem.option = 'EqualEnergy';
        waves.bem.count = 250;
        waves.phaseSeed = 1;
    otherwise
        waves = waveClass('irregular');         % Initialize Wave Class and Specify Type
        waves.height = 2.64;                     % Significant Wave Height [m]
        waves.period = 9.86;                       % Peak Period [s]
        waves.spectrumType = 'PM';              % Specify Spectrum Type
end
%waves.direction = [0,30,90];            % Wave Directionality [deg]
%waves.spread = [0.1,0.2,0.7];           % Wave Directional Spreading [%}

% % Irregular Waves with imported spectrum
% waves = waveClass('spectrumImport');      % Create the Wave Variable and Specify Type
% waves.spectrumFile = 'spectrumData.mat';  % Name of User-Defined Spectrum File [:,2] = [f, Sf]

% % Waves with imported wave elevation time-history  
% waves = waveClass('elevationImport');          % Create the Wave Variable and Specify Type
% waves.elevationFile = 'elevationData.mat';     % Name of User-Defined Time-Series File [:,2] = [time, eta]


%% Body Data
% Flap
body(1) = bodyClass('../../data/hydroData/oswec.h5');      % Initialize bodyClass for Flap
body(1).geometryFile = '../../data/geometry/flap.stl';     % Geometry File
body(1).mass = 127000;                          % User-Defined mass [kg]
body(1).inertia = [1.85e6 1.85e6 1.85e6];       % Moment of Inertia [kg-m^2]

if wave_type == 'YuJenne'
    body(1).morisonElement.option = 1;
    body(1).morisonElement.cd = ones (5,3);
    body(1).morisonElement.ca = zeros(5,3);
    body(1).morisonElement.area = zeros(5,3);
    body(1).morisonElement.area(:,1) = 18*1.8;
    body(1).morisonElement.area(:,3) = 18*1.8;
    body(1).morisonElement.VME  = zeros(5,1);
    body(1).morisonElement.rgME = [0 0 -3; 0 0 -1.2; 0 0 0.6; 0 0 2.4; 0 0 4.2];
    disp('Using Yu Jenne Morison stuff')
end

% Base
body(2) = bodyClass('../../data/hydroData/oswec.h5');      % Initialize bodyClass for Base
body(2).geometryFile = '../../data/geometry/base.stl';     % Geometry File
body(2).mass = 999;                             % Placeholder mass for a fixed body
body(2).inertia = [999 999 999];                % Placeholder inertia for a fixed body

%% PTO and Constraint Parameters
% Fixed
constraint(1)= constraintClass('Constraint1'); % Initialize ConstraintClass 
constraint(1).location = [0 0 -10];

% Rotationals
constraint(2)= constraintClass('Constraint2'); % Initialize ConstraintClass 
constraint(2).location = [0 0 -8.9];

constraint(3)= constraintClass('Constraint3'); % Initialize ConstraintClass 
constraint(3).location = [4.7021271782+0.9 0 -8.7];

constraint(4)= constraintClass('Constraint4'); % Initialize ConstraintClass 
constraint(4).location = [0+0.9 0 -7];

% Translational PTO
pto(1) = ptoClass('PTO1');                      % Initialize ptoClass for PTO1
pto(1).stiffness = 0;                           % PTO Stiffness Coeff [N/m]
pto(1).damping = 0;                         % PTO Damping Coeff [Ns/m]
pto(1).location = [2.35106397378+0.9 0 -7.849998936];   % PTO Global Location [m]
pto(1).orientation.z = [-4.7021271782/5 0 1.7/5];  % PTO orientation 