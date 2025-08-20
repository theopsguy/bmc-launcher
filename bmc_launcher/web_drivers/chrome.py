from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService


class ChromeWebDriver:
    def __init__(self, ignore_cert_errors: bool = False):
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        if ignore_cert_errors:
            chrome_options.add_argument("--ignore-certificate-errors")

        service = ChromeService()
        self.webdriver = webdriver.Chrome(service=service, options=chrome_options)

    def get_webdriver(self):
        return self.webdriver
