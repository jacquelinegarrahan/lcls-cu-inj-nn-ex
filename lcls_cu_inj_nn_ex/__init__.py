from . import _version
from pkg_resources import resource_filename
from lume_model.utils import variables_from_yaml
import pandas as pd 

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


CU_INJ_MAPPING = resource_filename(
    "lcls_cu_inj_nn_ex.files", "cu_inj_impact.csv"
)



with open(VARIABLE_FILE, "r") as f:
    INPUT_VARIABLES, OUTPUT_VARIABLES = variables_from_yaml(f)


CU_INJ_MAPPING_TABLE= pd.read_csv(CU_INJ_MAPPING)
CU_INJ_MAPPING_TABLE.set_index("impact_name")
