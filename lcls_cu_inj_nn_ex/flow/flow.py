from prefect import Flow, task
from prefect.storage import Docker
import time
import pandas as pd
from slac_services.services.scheduling import create_project, register_flow
import os
import sys
from prefect import Parameter
from prefect.engine import cache_validators
from prefect.run_configs import DockerRun
from lcls_cu_inj_nn_ex.model import LCLSCuInjNN
from datetime import timedelta
from contextlib import contextmanager
from pkg_resources import resource_filename
import tarfile
import os


@task(log_stdout=True, cache_for=timedelta(hours=1),
    cache_validator=cache_validators.all_parameters)
def predict(input_variables):
    model = LCLSCuInjNN()
    output_variables = model.evaluate(input_variables)
    return output_variables


def get_flow():
    dirname = os.path.dirname(__file__)

    # Requires a docker registry
    docker_registry = os.environ.get("DOCKER_REGISTRY")
    if not docker_registry:
        print("Requires docker registry to be set.")
        sys.exit()

    # THIS SHOULD BE CONVERTED INTO A UTILITY
    docker_storage = Docker(
        registry_url=docker_registry, 
        image_name="lcls-cu-inj-nn-ex",
        image_tag="latest",
       # path=os.path.dirname(__file__),
       # build_kwargs = {"nocache": True},
        stored_as_script=True,
        path=f"/opt/prefect/flow.py",
    )

    with Flow(
            "lcls-cu-inj-nn-ex",
            storage = docker_storage,
            run_config=DockerRun(image=f"{docker_registry}/lcls-cu-inj-nn-ex")
        ) as flow:
        input_variables = Parameter("input_variables")
        output_variables = predict(input_variables)

    docker_storage.add_flow(flow)

    return flow



if __name__ == "__main__":
    get_flow()