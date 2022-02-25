from setuptools import setup, find_packages
from os import path, environ
import versioneer

cur_dir = path.abspath(path.dirname(__file__))

# parse requirements
with open(path.join(cur_dir, "requirements.txt"), "r") as f:
    requirements = f.read().split()


setup(
    name="lcls_cu_inj_nn_ex",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="SLAC National Accelerator Laboratory",
    author_email="jgarra@slac.stanford.edu",
    license="SLAC Open",
    packages=find_packages(),
    install_requires=requirements,
    url="https://github.com/jacquelinegarrahan/lcls-cu-inj-nn-ex",
    include_package_data=True,
    python_requires=">=3.7",
    entry_points = {
        "orchestration": "model=lcls_cu_inj_nn_ex.model:LCLSCuInjNN"
    }
)
