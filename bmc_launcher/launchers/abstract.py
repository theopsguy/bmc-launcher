import logging
from abc import ABC, abstractmethod

from bmc_launcher.model.configuration import Server

log = logging.getLogger(__name__)


class BaseLauncher(ABC):
    def __init__(self, host: Server, driver):
        self.username = host.credentials.username
        self.password = host.credentials.password.get_secret_value()
        self.name = host.name
        self.url = host.url
        self.webdriver = driver

    @abstractmethod
    def launch(self):
        log.info(f"Launching browser to access {self.name} at {self.url}")
        pass
