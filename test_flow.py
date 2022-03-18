from lcls_cu_inj_nn_ex.flow.flow import get_flow

pvname_to_input_map = {
    "IRIS:LR20:130:CONFG_SEL": "distgen:r_dist:sigma_xy:value",
    "BPMS:IN20:221:TMIT": "distgen:total_charge:value",
    "SOLN:IN20:121:BACT": "SOL1:solenoid_field_scale",
    "QUAD:IN20:121:BACT": "CQ01:b1_gradient",
    "QUAD:IN20:122:BACT": "SQ01:b1_gradient",
    "ACCL:IN20:300:L0A_PDES": "L0A_phase:dtheta0_deg",
    "ACCL:IN20:400:L0B_PDES": "L0A_scale:voltage"

}

pv_values = {
    "IRIS:LR20:130:CONFG_SEL" :  0.4130,
    "BPMS:IN20:221:TMIT": 250.0,
    "SOLN:IN20:121:BACT" : 0.2460,
    "QUAD:IN20:121:BACT": -0.0074,
    "QUAD:IN20:122:BACT": -0.0074,
    "ACCL:IN20:300:L0A_PDES":  -0.0074,
    "ACCL:IN20:400:L0B_PDES": 70000000.0
}

settings = {
    "distgen:r_dist:sigma_xy:value": 0.4130,
    "distgen:t_dist:length:value" : 7.499772441611215,
    "end_mean_z": 4.6147002,
    "SOL1:solenoid_field_scale": 0.2460,
    "distgen:total_charge:value": 1.51614e+09,
    "CQ01:b1_gradient": -0.0074,
    "SQ01:b1_gradient": -0.0074,
    "L0A_phase:dtheta0_deg": -8.8997,
    "L0A_scale:voltage": 70000000.0
}

data = {
   # "pvname_to_input_map": pvname_to_input_map,
   # "pv_values": pv_values,
    "settings": settings
}

flow = get_flow()
flow.run(**data)
