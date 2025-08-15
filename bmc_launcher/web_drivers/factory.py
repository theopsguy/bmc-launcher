from bmc_launcher.web_drivers.chrome import ChromeWebDriver


def WebDriverFactory(driver_name: str, ignore_cert_errors: bool = False):
    drivers = {"chrome": ChromeWebDriver}

    return drivers[driver_name](ignore_cert_errors)
