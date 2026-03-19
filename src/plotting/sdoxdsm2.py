from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)

# Stage 1
x.add_system("opt1", OPT, r"\text{Genetic Algorithm}")
x.add_system("geom", FUNC, r"\text{Geometry}")
x.add_system("hydro", FUNC, r"\text{Hydrodynamics}")
x.add_system("lcoe", FUNC, r"\text{LCOE - Mechanical}")

# Stage 2
x.add_system("opt2", OPT, r"\text{Genetic Algorithm}")
x.add_system("desal", FUNC, r"\text{Desalination}")
x.add_system("solve", SOLVER, r"\text{ODE Solver}")
x.add_system("rigidbody", FUNC, r"\text{Rigid Body Dynamics}")
x.add_system("hydraulics", FUNC, r"\text{Hydraulics}")
x.add_system("econ", FUNC, r"\text{Economics}")

# Stage 3
x.add_system("opt3", OPT, r"\text{Genetic Algorithm}")
x.add_system("solve2", SOLVER, r"\text{ODE Solver}")
x.add_system("rigidbody2", FUNC, r"\text{Rigid Body Dynamics}")
x.add_system("hydraulics2", FUNC, r"\text{Hydraulics}")
x.add_system("econ2", FUNC, r"\text{Economics}")

# --- Overall sequential process order (SDO) ---
#x.add_process(
#    [
#        "opt1", "geom", "hydro", "opt2",
#        "solve", "rigidbody", "hydraulics", "opt3",
#        "desal", "econ", "opt1"   # loop back arrow to show overall workflow closure
#    ],
#    arrow=True,
#)

# === Stage 1 connections (opt1 -> geom, hydro) ===
x.connect("opt1", "geom", r"w,t,m")
x.connect("opt1", "hydro", r"w,t")
x.connect("geom", "hydro", r"\text{cg},V_{WEC},I")
x.connect("hydro", "lcoe", r"\begin{array}{c} f_e(\omega), K_{hs}, \\ A(\omega), B(\omega) \end{array}")
x.connect("opt1", "lcoe", r"w,t")
x.connect("lcoe", "opt1", r"LCOE")

# Stage 1 outputs feed into Stage 2 (and stage 3 later)
# geometry/hydro outputs become inputs to rigidbody & hydraulics
x.connect("hydro", "rigidbody", r"\begin{array}{c} f_e(\omega)^*, K_{hs}^*, \\ A(\omega)^*, B(\omega)^* \end{array}")
x.connect("geom", "rigidbody", r"\text{cg}^*,V_{WEC}^*,I^*")
x.connect("opt1", "rigidbody", r"m^*")
x.connect("geom", "rigidbody2", r"\text{cg}^*,V_{WEC}^*,I^*")
x.connect("hydro", "rigidbody2", r"\begin{array}{c} f_e(\omega)^*, K_{hs}^*, \\ A(\omega)^*, B(\omega)^* \end{array}")
x.connect("opt1", "rigidbody2", r"m^*")
x.connect("opt1","econ", r"w^*,t^*")
x.connect("opt1","econ2", r"w^*,t^*")


# === Stage 2 internal dynamics and solver usage ===
# Map optimizer outputs previously going to sysdyn -> now to rigidbody/hydraulics
x.connect("opt2", "desal", r"Q_{p,max}")
x.connect("opt2", "econ", r"Q_{p,max}")
x.connect("desal", "hydraulics", r"\begin{array}{c} \Delta \pi, R_m, R_t, \\ P_{relief} \end{array}")
x.connect("desal", "econ", r"Q_{f,max}")
x.connect("rigidbody", "hydraulics", r"\text{Piston Motion}")
x.connect("hydraulics", "rigidbody", r"\text{Force on Piston}")
x.connect("solve", "rigidbody", r"\text{Time Step}")
x.connect("solve", "hydraulics", r"\text{Time Step}")
x.connect("rigidbody", "econ", r"\text{stroke}")
x.connect("hydraulics","solve", r"\text{residuals}=0")
x.connect("rigidbody","solve", r"\text{residuals}=0")
x.connect("hydraulics","opt2",r"\text{Piston Pressure} \geq \text{min}")
x.connect("rigidbody","opt2",r"\text{Piston Motion} \leq \text{max}")
x.connect("hydraulics", "econ", r"Q_f, Q_p")
x.connect("econ", "opt2", r"\text{LCOW}")

# Feed optimal results to Stage 3:
x.connect("desal","hydraulics2", r"\begin{array}{c} \Delta \pi^*, R_m^*, R_t^*, \\ P^*_{relief} \end{array}")
x.connect("opt2", "econ2", r"Q^*_{p,max}")


# === Stage 3: Desalination & Economics ===
# Stage 3 optimizer drives desalination and economics
x.connect("opt3", "econ2", r"A_{p}, V_{acc}")
x.connect("opt3", "hydraulics2", r"A_{p}, V_{acc}, P_0")
x.connect("opt3", "rigidbody2", r"\ell_1")
x.connect("solve2", "rigidbody2", r"\text{Time Step}")
x.connect("solve2", "hydraulics2", r"\text{Time Step}")
x.connect("hydraulics2", "solve2", r"\text{residuals}=0 ")
x.connect("rigidbody2", "solve2", r"\text{residuals}=0")
x.connect("rigidbody2","hydraulics2", r"\text{Force on Piston}")
x.connect("hydraulics2","rigidbody2", r"\text{Piston Motion}")
x.connect("rigidbody2", "econ2", r"\text{stroke}")
x.connect("hydraulics2", "econ2", r"Q_f,Q_p")
x.connect("desal", "econ2", r"Q^*_{f,max}")
x.connect("econ2", "opt3", r"\text{LCOW}")
#x.connect("solve2", "opt3", r"\mathbf{g},\mathbf{h}")
x.connect("hydraulics2", "opt3", r"\text{Piston Pressure} \geq \text{min}")
x.connect("rigidbody2", "opt3", r"\text{Piston Motion} \leq \text{max}")

# === Inputs (preserve original inputs; route to appropriate stages) ===
x.add_input("geom", r"\text{draft}")
x.add_input("hydro", r"\text{draft}")
x.add_input("lcoe", r"\text{draft}, C_\text{ref}")
x.add_input("rigidbody", r"\text{draft}, \ell_2, \ell_3, \ell_{1,0}, \mathbf{p}_{\text{waves}}")
x.add_input("rigidbody2", r"\text{draft}, \ell_2, \ell_3, \mathbf{p}_{\text{waves}}")
x.add_input("hydraulics", r"A_{p,0}, V_{acc,0}, P_{0,0}")
x.add_input("desal", r"\begin{array}{c} \eta_{\text{RO}}, \mathbf{p}_{\text{seawater}}, \\ \mathbf{p}_{\text{membrane}} \end{array}")
x.add_input("econ", r"\begin{array}{c} \text{draft}, C_\text{ref}, \\ \mathbf{p}_{\text{plant}} \end{array}")
x.add_input("econ2", r"\begin{array}{c} \text{draft}, C_\text{ref}, \\ \mathbf{p}_{\text{plant}} \end{array}")

# === Outputs (stage optimizer results and final metrics) ===
x.add_output("opt1", r"\begin{array}{c} w_1^*,t_1^*,m_1^* \\ \text{(stage1 choices)} \end{array}", side=LEFT)
x.add_output("opt2", r"\begin{array}{c} Q_{p,max}^*\\ \text{(stage2 choices)} \end{array}", side=LEFT)
x.add_output("opt3", r"\begin{array}{c} \ell_{1}^*, A_{p,2}^*, V_{acc}^*, P_0^* \\ \text{(stage3 choice)} \end{array}", side=LEFT)

x.add_output("econ2", r"\text{LCOW}^*", side=LEFT)

# Finally write the SDO xDSM
x.write("xDSM_SDO2")
