% pressure = simout1.signal1;
% brine = simout1.signal3;
% perm = simout1.signal2;
% time = pressure.Time;
% pressure = pressure.Data;
% brine = brine.Data;
% perm = perm.Data;
% 
% % Define smoothing function (moving average)
% windowSize = 250; % Adjust as needed for smoothness
% smoothData = @(data) movmean(data, windowSize);
% 
% % Smooth data
% pressure = smoothData(pressure);
% brine = smoothData(brine);
% perm = smoothData(perm);
% 
% run get_colors.m
% figure('Name','Pressure')
% plot(time,pressure/1e6,'color',red,'linewidth',2)
% xlim([2400,2800])
% ylim([3.5,6])
% ylabel('Pressure (MPa)')
% title('')
% xlabel('Time (s)')
% figfix('Print1',14);
% fig_black();
% 
% figure('Name','flows')
% yyaxis left
% plot(time,perm,'color',blue,'linewidth',2,'displayname','Permeate','linestyle','-')
% hold on
% plot(time,brine,'color',red,'linewidth',2,'displayname','Brine','linestyle','-')
% plot(time,perm+brine,'color',purple,'linewidth',2,'displayname','Total','linestyle','-')
% ylabel('Flow Rate m^3/s')
% legend('Location','best')
% title('')
% xlabel('Time (s)')
% xlim([2400,2800])
% ylim([0,0.3])
% fig_black();
% 
% yyaxis right
% plot(time,perm./(perm+brine),'color',green,'linewidth',3,'displayname','Recovery Ratio','linestyle','-.')
% ylabel('Recovery Ratio')
% title('')
% ylim([0.1,0.35])
% figfix('Print4',14,1.5);
% fig_black();
