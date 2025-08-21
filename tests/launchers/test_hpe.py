from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr
from selenium.common.exceptions import TimeoutException

from bmc_launcher.launchers.hpe import HPELauncher
from bmc_launcher.model.configuration import Credentials, Manufacturer, Server


@pytest.fixture
def server():
    return Server(
        name="test_server",
        url="https://1.2.3.4",
        manufacturer=Manufacturer.hpe,
        credentials=Credentials(username="admin", password=SecretStr("password")),
    )


@patch("bmc_launcher.launchers.hpe.WebDriverWait")
def test_hpe_launcher_launch_success(mock_webdriver_wait, server):
    driver = MagicMock()
    iframe = MagicMock()
    username_input = MagicMock()
    password_input = MagicMock()
    login_button = MagicMock()

    mock_webdriver_wait.return_value.until.side_effect = [iframe, username_input]
    driver.find_element.side_effect = [password_input, login_button]

    launcher = HPELauncher(server, driver)
    launcher.launch()

    driver.get.assert_called_with("https://1.2.3.4")
    assert mock_webdriver_wait.return_value.until.call_count == 2
    driver.switch_to.frame.assert_called_with(iframe)
    username_input.send_keys.assert_called_with("admin")
    password_input.send_keys.assert_called_with("password")
    login_button.click.assert_called_once()


@patch("bmc_launcher.launchers.hpe.WebDriverWait")
def test_hpe_launcher_timeout(mock_wait, server):
    driver = MagicMock()
    mock_wait.return_value.until.side_effect = TimeoutException("Timeout occurred")

    launcher = HPELauncher(server, driver)
    with patch("sys.exit") as mock_exit:
        launcher.launch()
        mock_exit.assert_called_with(1)
