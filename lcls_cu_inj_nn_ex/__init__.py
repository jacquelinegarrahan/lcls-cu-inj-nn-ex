from . import _version
from pkg_resources import resource_filename
__version__ = _version.get_versions()['version']


MODEL_FILE = resource_filename(
    "lcls_cu_inj_nn_ex.files", "model_1b_AS_f_xy.h5"
)

VARIABLE_FILE =resource_filename(
    "lcls_cu_inj_nn_ex.files", "variables.yml"
)

EPICS_CONFIG_FILE =resource_filename(
    "lcls_cu_inj_nn_ex.files", "epics_config.yml"
)
