function [feedflow,permflow,time] = wdds_sim(hydro,wec_mass,wec_inertia,cg,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,mem_pressure_min,drivetrain_mass,wecSimOptions)
wave_type = 'degoede';

wecSim

time = simout1.signal1.Time;
feedflow = simout1.signal3.Data;
permflow = simout1.signal2.Data;
end