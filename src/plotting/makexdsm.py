from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT

x = XDSM(use_sfmath=True)

x.add_system("opt", OPT, r"\text{Genetic Algorithm}")
x.add_system("geom", FUNC, r"\text{Geometry}")
x.add_system("desal", FUNC, r"\text{Desalination}")
x.add_system("hydro", FUNC, r"\text{Hydrodynamics}")
x.add_system("sysdyn", FUNC, r"\text{System Dynamics}")
x.add_system("econ", FUNC, r"\text{Economics}")

x.add_process(
    ["opt", "geom", "desal", "hydro", "sysdyn", "econ", "opt"],
    arrow=True,
)

x.connect("opt", "geom", r"w,t,m")
x.connect("opt", "desal", r"Q_{p,max}")
x.connect("opt", "hydro", r"w,t")
x.connect("opt", "sysdyn", r"m,\ell_1,A_p,V_{acc}")
x.connect("opt", "econ", r"\begin{array}{c} w,t,\ell_1,A_p, \\ V_{acc},Q_{p,max} \end{array}")

x.connect("geom", "hydro", r"\text{cg},V_{WEC},I")
x.connect("geom", "sysdyn", r"\text{cg},V_{WEC},I")
x.connect("desal", "econ", r"Q_{f,max}")
x.connect("desal", "sysdyn", r"\begin{array}{c} \Delta \pi, R_m, R_t, \\ P_{relief} \end{array}")
x.connect("hydro", "sysdyn", r"\begin{array}{c} f_e(\omega), K_{hs}, \\ A(\omega), B(\omega) \end{array}")
x.connect("sysdyn", "econ", r"Q_{f},Q_{p},\text{stroke}")

x.connect("econ", "opt", r"\text{LCOW}")
x.connect("sysdyn", "opt", r"\mathbf{g},\mathbf{h}")

x.add_input("geom", r"\text{draft}")
x.add_input("desal", r"\begin{array}{c} \eta_{\text{RO}}, \mathbf{p}_{\text{seawater}}, \\ \mathbf{p}_{\text{membrane}} \end{array}")
x.add_input("hydro", r"\begin{array}{c} \text{draft} \end{array}")
x.add_input("sysdyn", r"\begin{array}{c} \text{draft}, \ell_2, \ell_3 \end{array}")
x.add_input("econ", r"\begin{array}{c} C_\text{ref}, \mathbf{p}_{\text{316SS}} \end{array}")

x.add_output("opt", r"\begin{array}{c} w^*,t^*,m^*,\ell_1^*,A_p^*, \\ V_{acc}^*,P_0^*,Q_{p,max}^* \end{array}", side=LEFT)
x.add_output("econ", r"\text{LCOW}^*", side=LEFT)

x.write("mdf")