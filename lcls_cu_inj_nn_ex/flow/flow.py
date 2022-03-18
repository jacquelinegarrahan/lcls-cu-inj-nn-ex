from prefect import Flow, task
from prefect.storage import Docker
import os
import sys
from prefect import Parameter
from prefect.engine.results import PrefectResult
from prefect.engine import cache_validators
from prefect.run_configs import KubernetesRun
from lcls_cu_inj_nn_ex.model import LCLSCuInjNN
import versioneer
from datetime import timedelta
import os
from lcls_cu_inj_nn_ex import INPUT_VARIABLES, CU_INJ_MAPPING_TABLE

dirname = os.path.dirname(__file__)



@task
def format_epics_input(pv_values, pvname_to_input_map):

    # check if any missing?
    missing_values = [pvname for pvname in pvname_to_input_map if pvname not in pv_values]
    if len(missing_values):
        raise ValueError(f"Missing pv values for {','.join(missing_values)}")

    input_variables = INPUT_VARIABLES
    # scale all values w.r.t. impact factor
    for pv_name, value in pv_values.items():
        var_name = pvname_to_input_map[pv_name]

        # if name included in scaling factors
        if (
            CU_INJ_MAPPING_TABLE["impact_name"]
            .str.contains(var_name, regex=False)
            .any()
        ):

            scaled_val = (
                value
                * CU_INJ_MAPPING_TABLE.loc[
                    CU_INJ_MAPPING_TABLE["impact_name"] == var_name, "impact_factor"
                ].item()
            )

            input_variables[var_name].value = scaled_val

        else:
            input_variables[var_name].value = value


    return input_variables


@task(log_stdout=True)
def model_predict(input_variables, settings):

    # settings are variables not read from epics
    for setting, value in settings.items():
        input_variables[setting].value = value

    model = LCLSCuInjNN()

    output_variables = model.evaluate(list(input_variables.values()))

    results = {
        var.name: var.value.astype('float64') for var in output_variables
    }

    results["x:y"] = results["x:y"].tolist()


    return results


docker_storage = Docker(
    registry_url="jgarrahan", 
    image_name="lcls-cu-inj-nn-ex",
    image_tag=versioneer.get_version(),
    # path=os.path.dirname(__file__),
    build_kwargs = {"nocache": True},
    stored_as_script=True,
    path=f"/opt/prefect/flow.py",
)


with Flow(
        "lcls-cu-inj-nn-ex",
        storage=docker_storage,
    ) as flow:


    input_variables = LCLSCuInjNN().input_variables


    pv_values = Parameter("pv_values", default={})
    pvname_to_input_map = Parameter("pvname_to_input_map", default={})
    settings = Parameter("settings", default={})
    input_variables = format_epics_input(pv_values, pvname_to_input_map)
    output_variables = model_predict(input_variables, settings)


docker_storage.add_flow(flow)


def get_flow():
    return flow
