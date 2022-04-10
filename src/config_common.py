import sys
from youwol_flux_backend import init_resources, Configuration as ServiceConfiguration
from youwol_utils.utils_paths import get_running_py_youwol_env

cache_prefix = "flux_backend_"


async def get_py_youwol_env():
    py_youwol_port = sys.argv[2]
    if not py_youwol_port:
        raise RuntimeError("The configuration requires py-youwol to run on port provided as command line option")
    return await get_running_py_youwol_env(py_youwol_port)


async def on_before_startup(selected_config: ServiceConfiguration):
    await init_resources(selected_config)
