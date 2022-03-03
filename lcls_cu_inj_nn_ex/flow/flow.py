from prefect import Flow, task
from prefect.storage import Docker
import os
import sys
from prefect import Parameter
from prefect.engine.results import PrefectResult
from prefect.engine import cache_validators
from prefect.run_configs import KubernetesRun
from lcls_cu_inj_nn_ex.model import LCLSCuInjNN
from datetime import timedelta
import os

dirname = os.path.dirname(__file__)




@task(log_stdout=True)
def predict(distgen_r_dist_sigma_xy_value, distgen_t_dist_length_value, distgen_total_charge_value, SOL1_solenoid_field_scale, CQ01_b1_gradient, SQ01_b1_gradient, L0A_phase_dtheta_deg, L0A_scale_voltage, end_mean_z):

    model = LCLSCuInjNN()

    input_variables["end_mean_z"].value = end_mean_z
    input_variables["L0A_scale:voltage"].value = L0A_scale_voltage
    input_variables["L0A_phase:dtheta0_deg"].value = L0A_phase_dtheta_deg
    input_variables["SQ01:b1_gradient"].value = SQ01_b1_gradient
    input_variables["CQ01:b1_gradient"].value = CQ01_b1_gradient
    input_variables["SOL1:solenoid_field_scale"].value = SOL1_solenoid_field_scale
    input_variables["distgen:total_charge:value"].value = distgen_total_charge_value
    input_variables["distgen:t_dist:length:value"].value = distgen_t_dist_length_value
    input_variables["distgen:r_dist:sigma_xy:value"].value = distgen_r_dist_sigma_xy_value

    output_variables = model.evaluate(input_variables)
    return {
        var.name: var.value for var in output_variables
    }


docker_storage = Docker(
    registry_url="jgarrahan", 
    image_name="lcls-cu-inj-nn-ex",
    image_tag="latest",
    # path=os.path.dirname(__file__),
    # build_kwargs = {"nocache": True},
    stored_as_script=True,
    path=f"/opt/prefect/flow.py",
)


input_variables = LCLSCuInjNN().input_variables
with Flow(
        "lcls-cu-inj-nn-ex",
        storage = docker_storage,
        run_config=KubernetesRun(image="jgarrahan/lcls-cu-inj-nn-ex", image_pull_policy="Always"),
        result=PrefectResult()
    ) as flow:


    params = []
    for var in input_variables.values():


        params.append(Parameter(var.name, default=var.default))
    
    output_variables = predict(distgen_r_dist_sigma_xy_value, distgen_t_dist_length_value, distgen_total_charge_value, SOL1_solenoid_field_scale, CQ01_b1_gradient, SQ01_b1_gradient, L0A_phase_dtheta_deg, L0A_scale_voltage, end_mean_z)
    result = format_output(output_variables)

docker_storage.add_flow(flow)



def get_flow():
    return flow
