from pathlib import Path
from config_common import get_py_youwol_env, on_before_startup
from youwol_flux_backend import Constants, Configuration
from youwol_utils import LocalStorageClient, LocalDocDbClient
from youwol_utils.clients.assets_gateway.assets_gateway import AssetsGatewayClient
from youwol_utils.context import ConsoleContextLogger
from youwol_utils.http_clients.flux_backend import PROJECTS_TABLE, COMPONENTS_TABLE
from youwol_utils.middlewares.authentication_local import AuthLocalMiddleware
from youwol_utils.servers.fast_api import FastApiMiddleware, AppConfiguration, ServerOptions


async def get_configuration():
    env = await get_py_youwol_env()
    databases_path = Path(env['pathsBook']['databases'])

    async def _on_before_startup():
        await on_before_startup(service_config)

    service_config = Configuration(
        storage=LocalStorageClient(root_path=databases_path / 'storage',
                                   bucket_name=Constants.namespace),
        doc_db=LocalDocDbClient(root_path=databases_path / 'docdb',
                                keyspace_name=Constants.namespace,
                                table_body=PROJECTS_TABLE
                                ),
        doc_db_component=LocalDocDbClient(
            root_path=databases_path.parent / 'docdb',
            keyspace_name=Constants.namespace,
            table_body=COMPONENTS_TABLE
        ),
        assets_gtw_client=AssetsGatewayClient(url_base=f"http://localhost:{env['httpPort']}/api/assets-gateway")
    )
    server_options = ServerOptions(
        root_path="",
        http_port=env['portsBook']['flux-backend'],
        base_path="",
        middlewares=[FastApiMiddleware(AuthLocalMiddleware, {})],
        on_before_startup=_on_before_startup,
        ctx_logger=ConsoleContextLogger()
    )
    return AppConfiguration(
        server=server_options,
        service=service_config
    )
