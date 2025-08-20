from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr
from selenium.common.exceptions import TimeoutException

from bmc_launcher.launchers.supermicro import SupermicroLauncher
from bmc_launcher.model.configuration import Credentials, Manufacturer, Server


@pytest.fixture
def server():
    return Server(
        name="test_server",
        url="http://1.2.3.4",
        manufacturer=Manufacturer.supermicro,
        credentials=Credentials(username="admin", password=SecretStr("password")),
    )


@patch("bmc_launcher.launchers.supermicro.WebDriverWait")
def test_supermicro_launcher_launch_success(mock_webdriver_wait, server):
    driver = MagicMock()
    username_input = MagicMock()
    password_input = MagicMock()
    login_button = MagicMock()

    mock_webdriver_wait.return_value.until.return_value = username_input
    driver.find_element.side_effect = [password_input, login_button]

    launcher = SupermicroLauncher(server, driver)
    launcher.launch()

    driver.get.assert_called_with("http://1.2.3.4")
    username_input.send_keys.assert_called_with("admin")
    password_input.send_keys.assert_called_with("password")
    login_button.click.assert_called_once()


@patch("bmc_launcher.launchers.supermicro.WebDriverWait")
def test_supermicro_launcher_timeout(mock_wait, server):
    driver = MagicMock()
    mock_wait.return_value.until.side_effect = TimeoutException("Timeout occurred")

    launcher = SupermicroLauncher(server, driver)
    with patch("sys.exit") as mock_exit:
        launcher.launch()
        mock_exit.assert_called_with(1)
