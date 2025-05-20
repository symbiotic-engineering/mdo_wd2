function [result] = solveIRFs_par(hydro, key)
result = parfeval(@solveIRFs_key, 2, hydro, key);
end