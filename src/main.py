import asyncio

import uvicorn
from fastapi import FastAPI, Depends

from youwol_flux.configurations import get_configuration, Configuration
from youwol_flux.root_paths import router as flux_router
from youwol_flux.utils import init_resources
from youwol_utils import log_info
from youwol_utils.middlewares.root_middleware import RootMiddleware
from youwol_utils.utils_paths import matching_files, FileListing, files_check_sum

configuration: Configuration = asyncio.get_event_loop().run_until_complete(get_configuration())
asyncio.get_event_loop().run_until_complete(init_resources(configuration))

app = FastAPI(
    title="flux-backend",
    description="description",
    openapi_prefix=configuration.open_api_prefix)

app.add_middleware(configuration.auth_middleware, **configuration.auth_middleware_args)
app.add_middleware(RootMiddleware, ctx_logger=configuration.ctx_logger)

app.include_router(
    flux_router,
    prefix=configuration.base_path,
    dependencies=[Depends(get_configuration)],
    tags=[]
)

files_src_check_sum = matching_files(
    folder="./",
    patterns=FileListing(
        include=['*'],
        # when deployed using dockerfile there is additional files in ./src: a couple of .* files and requirements.txt
        ignore=["requirements.txt", ".*", "*.pyc"]
    )
)

log_info(f"./src check sum: {files_check_sum(files_src_check_sum)} ({len(files_src_check_sum)} files)")

if __name__ == "__main__":
    # app: incorrect type. More here: https://github.com/tiangolo/fastapi/issues/3927
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=configuration.http_port)
