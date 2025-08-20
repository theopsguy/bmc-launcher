from unittest.mock import MagicMock, patch

import pytest

from bmc_launcher.web_drivers.chrome import ChromeWebDriver


@pytest.fixture
def mock_chrome_service():
    with patch("bmc_launcher.web_drivers.chrome.ChromeService") as mock:
        yield mock


@pytest.fixture
def mock_chrome_options():
    with patch("bmc_launcher.web_drivers.chrome.ChromeOptions") as mock:
        yield mock


@pytest.fixture
def mock_webdriver():
    with patch("bmc_launcher.web_drivers.chrome.webdriver") as mock:
        yield mock


def test_chrome_webdriver_init_default(mock_chrome_service, mock_chrome_options, mock_webdriver):
    driver = ChromeWebDriver()
    mock_chrome_options.return_value.add_experimental_option.assert_called_once_with("detach", True)
    mock_chrome_options.return_value.add_argument.assert_not_called()
    mock_webdriver.Chrome.assert_called_once()


def test_chrome_webdriver_init_ignore_certs(mock_chrome_service, mock_chrome_options, mock_webdriver):
    driver = ChromeWebDriver(ignore_cert_errors=True)
    mock_chrome_options.return_value.add_experimental_option.assert_called_once_with("detach", True)
    mock_chrome_options.return_value.add_argument.assert_called_once_with("--ignore-certificate-errors")
    mock_webdriver.Chrome.assert_called_once()


def test_get_webdriver(mock_chrome_service, mock_chrome_options, mock_webdriver):
    driver = ChromeWebDriver()
    webdriver_instance = driver.get_webdriver()
    assert webdriver_instance == mock_webdriver.Chrome.return_value
