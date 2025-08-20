import logging
import sys

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bmc_launcher.launchers.abstract import BaseLauncher
from bmc_launcher.model.configuration import Server

log = logging.getLogger(__name__)


class SupermicroLauncher(BaseLauncher):
    def __init__(self, host: Server, driver):
        super().__init__(host, driver)

    def launch(self):
        super().launch()
        self.webdriver.get(self.url)

        try:
            username_input = WebDriverWait(self.webdriver, 10).until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )

            username_input.send_keys(self.username)
            password_input = self.webdriver.find_element(By.NAME, "pwd")
            password_input.send_keys(self.password)

            self.webdriver.find_element(By.ID, "login_word").click()
            log.info("Login submitted.")
        except (TimeoutException, NoSuchElementException) as e:
            log.error(f"Login page interaction failed: {e}")
            sys.exit(1)
