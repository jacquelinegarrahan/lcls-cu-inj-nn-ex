from prefect import Flow, task
from prefect.storage import Docker
import time
import pandas as pd
from slac_services.services.scheduling import create_project, register_flow
import os
import sys
from prefect import Parameter
from prefect.engine import cache_validators
from lcls_cu_inj_nn_ex.model import LCLSCuInjNN
from datetime import timedelta
from contextlib import contextmanager
from pkg_resources import resource_filename
import tarfile



DOCKERFILE = resource_filename(
    "lcls_cu_inj_nn_ex.flow", "Dockerfile"
)


@contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with working_directory('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)




@task(log_stdout=True, cache_for=timedelta(hours=1),
    cache_validator=cache_validators.all_parameters)
def predict(input_variables):
    model = LCLSCuInjNN()
    output_variables = model.evaluate(input_variables)
    return output_variables


def build_flow():
    dirname = os.path.dirname(__file__)

    # Requires a docker registry
    docker_registry = os.environ.get("DOCKER_REGISTRY")
    if not docker_registry:
        print("Requires docker registry to be set.")
        sys.exit()

    with tarfile.open("tmp.tar.gz", "w") as tar_handle:
        for file in os.listdir(dirname):
            tar_handle.add(f"{dirname}/{file}", arcname=file)

    with working_directory(dirname) as cwd:
        flow = Flow(
            "lcls-cu-inj-nn-ex",
            storage=Docker(
                registry_url=docker_registry, 
                image_name="lcls-cu-inj-nn-ex",
                dockerfile="Dockerfile",
                build_kwargs = {"nocache": True}
            )
        )

    with flow:
        input_variables = Parameter("input_variables")
        output_variables = predict(input_variables)

    return flow


if __name__ == "__main__":
    build_flow()