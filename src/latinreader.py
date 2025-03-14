import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
import openmdao.api as om
from src.runner import RunWDDS

cr = om.CaseReader("run_latin_out/cases.sql")
cases = cr.list_cases('driver',recurse=True)
print(cases)
dvs = ["width","thickness","wec_mass","hinge2joint","piston_area","accum_volume","accum_P0","capacity","LCOW"]
#dvs = ["LCOW"]
vars_values = {var:[cr.get_case(case).outputs[var] for case in cases ] for var in dvs }

print(vars_values)