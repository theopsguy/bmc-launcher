from bmc_launcher.launchers.dell_idrac8 import DellIdrac8Launcher
from bmc_launcher.launchers.dell_idrac9 import DellIdrac9Launcher
from bmc_launcher.launchers.hpe import HPELauncher
from bmc_launcher.launchers.supermicro import SupermicroLauncher
from bmc_launcher.model.configuration import DellServer, HPEServer, Server, SupermicroServer

LAUNCHER_REGISTRY = {
    HPEServer: {
        4: HPELauncher,
    },
    DellServer: {
        8: DellIdrac8Launcher,
        9: DellIdrac9Launcher,
    },
    SupermicroServer: {
        None: SupermicroLauncher,
    },
}


def create_launcher(server: Server, driver):
    server_type = type(server)
    versions = LAUNCHER_REGISTRY.get(server_type)
    if not versions:
        raise ValueError(f"No launcher for manufacturer: {server.manufacturer.value}")

    launcher_cls = versions.get(server.bmc_version)
    if not launcher_cls:
        raise ValueError(f"No launcher for {server.manufacturer.value} version {server.bmc_version}")

    return launcher_cls(server, driver)
