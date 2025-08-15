import sys
import logging

from bmc_launcher.model.configuration import Server
from bmc_launcher.launchers.abstract import BaseLauncher
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


class HPELauncher(BaseLauncher):
    def __init__(self, host: Server, driver):
        super().__init__(host, driver)

    def launch(self):
        log.info(f"Launching browser to access {self.name} at {self.url}")
        self.webdriver.get(self.url)
        try:
            iframe = WebDriverWait(self.webdriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.webdriver.switch_to.frame(iframe)

            username_input = WebDriverWait(self.webdriver, 10).until(
                EC.visibility_of_element_located((By.ID, "usernameInput"))
            )
            username_input.send_keys(self.username)
            password_input = self.webdriver.find_element(By.ID, "passwordInput")
            password_input.send_keys(self.password)

            self.webdriver.find_element(By.ID, "ID_LOGON").click()
            log.info("Login submitted.")
        except (TimeoutException, NoSuchElementException) as e:
            log.error(f"Login page interaction failed: {e}")
            sys.exit(1)
