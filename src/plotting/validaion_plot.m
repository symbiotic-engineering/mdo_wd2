clear; clc; close all;

%% Load data
% My version
load ../../data/validation/myVersion_smalldt.mat
pressure1 = simout1.signal1;
brine1 = simout1.signal3;
perm1 = simout1.signal2;
time1 = pressure1.Time;
pressure1 = pressure1.Data;
brine1 = brine1.Data;
perm1 = perm1.Data;

% load ../../data/validation/myVersion_startSteady.mat
% pressure2 = simout1.signal1;
% brine2 = simout1.signal3;
% perm2 = simout1.signal2;
% time2 = pressure2.Time;
% pressure2 = pressure2.Data;
% brine2 = brine2.Data;
% perm2 = perm2.Data;

% WEC-Sim Applications Results
% load ../../data/validation/wecSimAppsVersion.mat
% pressure1 = simout1.signals.values(:,6);
% brine1 = simout1.signals.values(:,3);
% perm1 = simout1.signals.values(:,2);
% time1 = simout1.time;
load ../../data/validation/wecSimApps_nolocalnosteady.mat
pressure2 = simout1.signals.values(:,6);
brine2 = simout1.signals.values(:,3);
perm2 = simout1.signals.values(:,2);
time2 = simout1.time;

% Paper
run ../../data/validation/plot_digitize/read_data.m

%% Define smoothing function
%windowSize1 = 50; % My version
%windowSize2 = 2;  % WEC-Sim version
%smoothData = @(data, windowSize) movmean(data, windowSize);

% Smooth data
%pressure1 = smoothData(pressure1, windowSize1);
%brine1 = smoothData(brine1, windowSize1);
%perm1 = smoothData(perm1, windowSize1);

%pressure2 = smoothData(pressure2, windowSize2);
%brine2 = smoothData(brine2, windowSize2);
%perm2 = smoothData(perm2, windowSize2);

run get_colors.m

%% Plot Pressure
figure('Name', 'Pressure');
hold on;
plot(time3_pressure, pressure3/10, 'color', black, 'linewidth', 2, 'linestyle', 'None', 'DisplayName', 'Yu & Jenne','Marker','x');
plot(time1, pressure1 / 1e6, 'color', red, 'linewidth', 2, 'DisplayName', 'Mine');
plot(time2, pressure2 / 1e6, 'color', blue, 'linewidth', 2, 'linestyle', '--', 'DisplayName', 'WEC-Sim');
hold off;
xlim([2400, 2800]);
ylim([3.5, 6]);
ylabel('Pressure (MPa)');
xlabel('Time (s)');
legend('Location', 'best');
title('Pressure Comparison');
figfix('Print1', 14);
%fig_black();

%% Plot Flows
figure('Name', 'Flows');
yyaxis left;
hold on;
plot(time3_perm, perm3, 'color',black,'linewidth', 2, 'DisplayName', 'Permeate (Yu & Jenne)', 'linestyle', 'None','Marker','x');
plot(time3_total, total3, 'color',black,'linewidth', 2, 'DisplayName', 'Total (Yu & Jenne)', 'linestyle', 'None','Marker','+');
plot(time1, perm1, 'color', blue, 'linewidth', 2, 'DisplayName', 'Permeate (Mine)', 'linestyle', '-');
plot(time1, brine1+perm1, 'color', red, 'linewidth', 2, 'DisplayName', 'Total (Mine)', 'linestyle', '-');
plot(time2, perm2, 'color', skyblue, 'linewidth', 2, 'DisplayName', 'Permeate (WEC-Sim)', 'linestyle', '--','Marker','None');
plot(time2, brine2+perm2, 'color', orange, 'linewidth', 2, 'DisplayName', 'Total (WEC-Sim)', 'linestyle', '--','Marker','None');
ylabel('Flow Rate (m^3/s)');
ylim([0, 0.3]);
%fig_black();

yyaxis right;
plot(time3_recovery, recovery3, 'color',black,'linewidth', 2, 'DisplayName', 'Recovery Ratio (Yu & Jenne)', 'linestyle', 'None','Marker','^');
plot(time1, perm1 ./ (perm1 + brine1), 'color', green, 'linewidth', 2, 'DisplayName', 'Recovery Ratio (Mine)', 'linestyle', '-');
plot(time2, perm2 ./ (perm2 + brine2), 'color', purple, 'linewidth', 2, 'DisplayName', 'Recovery Ratio (WEC-Sim)', 'linestyle', '--');
ylabel('Recovery Ratio');
ylim([0.1, 0.35]);

legend('Location', 'best');
title('Flow and Recovery Ratio Comparison');
xlabel('Time (s)');
xlim([2500, 2700]);
figfix('Print4', 14, 1.5);
%fig_black();
hold off;

percentError = calculatePercentError(time2,perm2, time1,perm1,2500,2700);
wsa_mine_error = mean(percentError)

percentError = calculatePercentError(time3_perm,perm3, time2,perm2,2500,2700);
wsa_yj_error = mean(percentError)

percentError = calculatePercentError(time3_perm,perm3, time1,perm1,2500,2700);
yj_mine_error = mean(percentError)

function percentError = calculatePercentError(referenceTime, referenceData, testTime, testData, startTime, endTime)
    % CALCULATEPERCENTERRORINRANGE Computes the percent error within a specific time range.
    %
    % Inputs:
    %   referenceTime - Time vector for the reference dataset (e.g., WEC-Sim time).
    %   referenceData - Reference dataset (e.g., WEC-Sim data).
    %   testTime      - Time vector for the test dataset (e.g., "My Version" time).
    %   testData      - Test dataset (e.g., "My Version" data).
    %   startTime     - Start of the time range for error calculation.
    %   endTime       - End of the time range for error calculation.
    %
    % Output:
    %   percentError  - Percent error for the test dataset interpolated onto the reference time vector within the specified range.

    % Filter reference data to the specified time range
    rangeMask = (referenceTime >= startTime) & (referenceTime <= endTime);
    referenceTimeInRange = referenceTime(rangeMask);
    referenceDataInRange = referenceData(rangeMask);

    % Interpolate the test data onto the reference time vector within the range
    testDataInterp = interp1(testTime, testData, referenceTimeInRange, 'linear', 'extrap');

    % Calculate percent error within the range
    percentError = abs((testDataInterp - referenceDataInRange) ./ referenceDataInRange) * 100;
end

