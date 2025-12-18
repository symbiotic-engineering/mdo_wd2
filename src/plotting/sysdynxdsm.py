from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)

x.add_system("solve", SOLVER, r"\text{ODE Solver}")
x.add_system("rigidbody", FUNC, r"\text{Rigid Body Dynamics}")
x.add_system("hydraulics", FUNC, r"\text{Hydraulics}")



x.connect("rigidbody", "hydraulics", r"\text{Piston Motion}")
x.connect("hydraulics", "rigidbody", r"\text{Force on Piston}")
x.connect("solve","rigidbody",r"\text{Time}")
x.connect("solve","hydraulics",r"\text{Time}")
x.connect("hydraulics","solve",r"\begin{array}{c}\text{Piston Pressure} \geq \text{min}, \\ \text{residuals}=0 \end{array}")
x.connect("rigidbody","solve",r"\begin{array}{c}\text{Piston Motion} \leq \text{max}, \\ \text{residuals}=0 \end{array}")

x.add_input("rigidbody", r"\begin{array}{c} \text{draft}, \ell_2, \ell_3, m, \ell_1, \text{cg}, V_{WEC}, \\ I, f_e(\omega), K_{hs}, A(\omega), B(\omega) \end{array}")
x.add_input("hydraulics", r"\begin{array}{c} A_p, V_{acc}, \Delta \pi, \\ R_m, R_t, P_{relief} \end{array}")

x.add_output("hydraulics",r"Q_f,Q_p",side=RIGHT)
x.add_output("rigidbody",r"\text{stroke}",side=RIGHT)

x.write("xDSM_sysdyn")