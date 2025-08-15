from bmc_launcher.model.configuration import Server
from bmc_launcher.launchers.hpe import HPELauncher


def SeleniumFactory(server: Server, driver):
    launchers = {
        ("HPE", 4): HPELauncher,
    }

    manufacturer = server.manufacturer.upper()
    version = None

    if manufacturer == "HPE":
        version = server.ilo_version

    # Determine the key
    key = (manufacturer, version)

    if key not in launchers:
        raise ValueError(f"No launcher found for {key}")

    return launchers[key](server, driver)
