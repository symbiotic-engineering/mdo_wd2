function [feedflow,permflow,time,pressure,key] = wdds_sim(hydro,wec_mass,wec_inertia,hinge_depth,joint_depth,intake_x,intake_z,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,osmotic_pressure,drivetrain_mass,wecSimOptions,key)
wave_type = 'degoede';
%profile on;
wecSim
%profile off;
%profile viewer; % Open the interactive profiler interface
time = simout1.signal1.Time;
pressure = simout1.signal1.Data;
feedflow = simout1.signal3.Data;
permflow = simout1.signal2.Data;
end