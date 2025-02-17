function [result] = wdds_par(hydro,wec_mass,wec_inertia,cg,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,mem_pressure_min,drivetrain_mass,wecSimOptions)
result = parfeval(@wdds_sim, 3, hydro,wec_mass,wec_inertia,cg,piston_area,piston_stroke,accum_volume,accum_P0,pressure_relief,throt_resist,mem_resist,mem_pressure_min,drivetrain_mass,wecSimOptions);
end