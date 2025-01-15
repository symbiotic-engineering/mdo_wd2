function [CAPEX,OPEX] = ro_econ(production,capacity,ro_econ_params)
	I_RO = ro_econ_params.I_RO;	# [$/(m^3/day]	nominally 1,177
	CAPEX = capacity*I_RO		# [$]

	labor_rate = ro_econ_params.labor;	# [$/laborer]	nominally 29,700
	manag_rate = ro_econ_params.manag;	# [$/manager]	nominally 66,000
	unit_opex = ro_econ_params.unitopex;	# [$/m^3]	nominally 0.15
	insur_rate = ro_econ_params.insur_rate;	# [%]		nominally 0.5
	
	Nlaborers = (capacity*264/6e6)^0.4 + 18/1.4;	# 	Number of laborers
	Nmanagers = (5+capacity/55000)/2		#	Number of managers

	OPEX = Nlaborers*labor_rate + Nmanagers*manag_rate + inusr_rate*CAPEX + production*unit_opex;
end
