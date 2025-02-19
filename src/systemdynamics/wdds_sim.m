function [feedflow,permflow,time,key] = wdds_sim(hydro,wec_mass,wec_inertia,cg,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,mem_pressure_min,drivetrain_mass,wecSimOptions,key)
wave_type = 'degoede';
profile on;
wecSim
profile off;
profsave(profile('info'), 'profile_results'); % Save the report to disk
time = simout1.signal1.Time;
feedflow = simout1.signal3.Data;
permflow = simout1.signal2.Data;
end