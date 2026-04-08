import logging
import sys

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bmc_launcher.launchers.abstract import BaseLauncher
from bmc_launcher.model.configuration import Server

log = logging.getLogger(__name__)


class DellIdrac9Launcher(BaseLauncher):
    def __init__(self, host: Server, driver):
        super().__init__(host, driver)

    def launch(self):
        super().launch()
        self.webdriver.get(self.url)

        try:
            WebDriverWait(self.webdriver, 30).until(EC.visibility_of_element_located((By.NAME, "username")))
            username_input = self.webdriver.find_element("name", "username")
            password_input = self.webdriver.find_element("name", "password")

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)

            WebDriverWait(self.webdriver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "cux-button")))
            self.webdriver.find_element(By.CLASS_NAME, "cux-button").click()
            log.info("Login submitted.")
        except (TimeoutException, NoSuchElementException) as e:
            log.error("Login page interaction failed: %s", e)
            sys.exit(1)
