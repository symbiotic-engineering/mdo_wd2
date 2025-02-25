function [feedflow,permflow,time,key] = wdds_sim(hydro,wec_mass,wec_inertia,wec_thickness,hinge_depth,joint_depth,intake_x,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,osmotic_pressure,drivetrain_mass,wecSimOptions,key)
wave_type = 'degoede';
%profile on;
wecSim
%profile off;
%profile viewer; % Open the interactive profiler interface
time = simout1.signal1.Time;
feedflow = simout1.signal3.Data;
permflow = simout1.signal2.Data;
end