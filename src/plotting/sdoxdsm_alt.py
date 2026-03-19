from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)

# Top-level MDO systems (with sysdyn expanded below)
x.add_system("opt1", OPT, r"\text{Genetic Algorithm}")
x.add_system("geom", FUNC, r"\text{Geometry}")
x.add_system("hydro", FUNC, r"\text{Hydrodynamics}")
x.add_system("opt2", OPT, r"\text{Genetic Algorithm}")
x.add_system("solve", SOLVER, r"\text{ODE Solver}")
x.add_system("rigidbody", FUNC, r"\text{Rigid Body Dynamics}")
x.add_system("piston", FUNC, r"\text{Piston}")
x.add_system("opt3", OPT, r"\text{Genetic Algorithm}")
x.add_system("desal", FUNC, r"\text{Desalination}")
x.add_system("swro", FUNC, r"\text{SWRO Hydraulics}")
x.add_system("econ", FUNC, r"\text{Economics}")

#x.add_group(
#    "sysdyn_cluster",
#    ["solve", "rigidbody", "hydraulics"],
#    r"\text{System Dynamics}"
#)

# Overall process order (keeps the diagonal flow)
#x.add_process(
#    ["opt", "geom", "desal", "hydro", "solve", "rigidbody", "hydraulics", "econ", "opt"],
#    arrow=True,
#)

# Connections from optimizer to design blocks
x.connect("opt1", "geom", r"w,t,m")
x.connect("opt3", "desal", r"Q_{p,max}")
x.connect("opt1", "hydro", r"w,t")
x.connect("opt1","rigidbody", r"m^*")

# Map optimizer outputs previously going to sysdyn -> now to rigidbody/hydraulics
x.connect("opt2", "rigidbody", r"\ell_1")
x.connect("opt2", "piston", r"A_p")

# Geometry outputs: geometry -> hydrodynamics (unchanged) and geometry -> rigidbody (was sysdyn)
x.connect("geom", "hydro", r"\text{cg},V_{WEC},I")
x.connect("geom", "rigidbody", r"\text{cg},V_{WEC},I")

# Desalination connections: desal -> econ (unchanged) and desal -> hydraulics (was sysdyn)
x.connect("desal", "econ", r"Q_{f,max}")
x.connect("desal", "hydraulics", r"\begin{array}{c} \Delta \pi, R_m, R_t, \\ P_{relief} \end{array}")

# Hydrodynamics -> rigidbody (was hydro -> sysdyn)
x.connect("hydro", "rigidbody", r"\begin{array}{c} f_e(\omega), K_{hs}, \\ A(\omega), B(\omega) \end{array}")

# Internal dynamics connections (from second XDSM)
x.connect("rigidbody", "hydraulics", r"\text{Piston Motion}")
x.connect("hydraulics", "rigidbody", r"\text{Force on Piston}")

# Solver interactions: solver provides Time to both; hydraulics & rigidbody return residuals & constraints
x.connect("solve", "rigidbody", r"\text{Time}")
x.connect("solve", "hydraulics", r"\text{Time}")

x.connect("hydraulics", "solve", r"\begin{array}{c}\text{Piston Pressure} \geq \text{min}, \\ \text{residuals}=0 \end{array}")
x.connect("rigidbody", "solve", r"\begin{array}{c}\text{Piston Motion} \leq \text{max}, \\ \text{residuals}=0 \end{array}")

# Dynamics outputs -> economics (match original sysdyn->econ mapping)
x.connect("hydraulics", "econ", r"Q_{f},Q_{p}")
x.connect("rigidbody", "econ", r"\text{stroke}")

# Constraints from solver -> optimizer (g,h)
x.connect("solve", "opt", r"\mathbf{g},\mathbf{h}")

# Reconnect sysdyn outputs to optimizer/econ as they were originally:
# (Note: earlier sysdyn->opt and sysdyn->econ are now mapped to solve/rigidbody/hydraulics)
x.connect("econ", "opt", r"\text{LCOW}")

# Inputs (preserve the original top-level inputs and route them to the expanded blocks)
x.add_input("geom", r"\text{draft}")
x.add_input("desal", r"\begin{array}{c} \eta_{\text{RO}}, \mathbf{p}_{\text{seawater}}, \\ \mathbf{p}_{\text{membrane}} \end{array}")
x.add_input("hydro", r"\begin{array}{c} \text{draft} \end{array}")

x.add_input("rigidbody", r"\text{draft}, \ell_2, \ell_3")
x.add_input("solve",r"\text{sea state}")

# Outputs: keep original optimizer/econ outputs
x.add_output("opt", r"\begin{array}{c} w^*,t^*,m^*,\ell_1^*,A_p^*, \\ V_{acc}^*,P_0^*,Q_{p,max}^* \end{array}", side=LEFT)
x.add_output("econ", r"\text{LCOW}^*", side=LEFT)

# Dynamics outputs (placed on the right as in your second XDSM)
#x.add_output("hydraulics", r"Q_f,Q_p", side=RIGHT)
#x.add_output("rigidbody", r"\text{stroke}", side=RIGHT)

# Write merged XDSM
x.write("xDSM_merged")
