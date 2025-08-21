import pytest
from pydantic import SecretStr, ValidationError

from bmc_launcher.model.configuration import (
    Configuration,
    Credentials,
    DellServer,
    Manufacturer,
    Server,
    SupermicroServer,
)


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin", SecretStr("secret"), "**********"),
        (None, None, None),
        ("user", None, None),
        ("", SecretStr("pass"), "**********"),
        ("", None, None),
    ],
)
def test_credentials_mask_password(username, password, expected):
    creds = Credentials(username=username, password=password)
    assert creds.model_dump()["password"] == expected


@pytest.mark.parametrize(
    "manufacturer,should_error",
    [
        ("DELL", False),
        ("HPE", False),
        ("SUPERMICRO", False),
        ("UNKNOWN", True),
    ],
)
def test_server_enum_validation(manufacturer, should_error):
    if should_error:
        with pytest.raises(ValidationError):
            Server(
                name="test_server",
                url="https://1.2.3.4",
                manufacturer=manufacturer,
            )
    else:
        Server(
            name="test_server",
            url="https://1.2.3.4",
            manufacturer=manufacturer,
        )


def test_get_credentials_prefers_server_over_default():
    default_creds = {Manufacturer.hpe: Credentials(username="default", password=SecretStr("defaultpw"))}
    server = Server(
        name="web00",
        url="https://192.168.1.10",
        manufacturer=Manufacturer.hpe,
        credentials=Credentials(username="admin", password=SecretStr("pw")),
    )
    creds = server.get_credentials(default_creds)
    assert creds.username == "admin"
    assert creds.password.get_secret_value() == "pw"


def test_get_credentials_uses_default_if_missing():
    default_creds = {Manufacturer.hpe: Credentials(username="default", password=SecretStr("defaultpw"))}
    server = Server(
        name="web00",
        url="https://192.168.1.10",
        manufacturer=Manufacturer.hpe,
        credentials=None,
    )
    creds = server.get_credentials(default_creds)
    assert creds.username == "default"
    assert creds.password.get_secret_value() == "defaultpw"


def test_configuration_mode_empty_hosts():
    # Test with empty hosts and one default credential
    config = Configuration(
        hosts=[], default_credentials={Manufacturer.dell: Credentials(username="root", password=SecretStr("dellpass"))}
    )

    assert isinstance(config.hosts, list)
    assert isinstance(config.default_credentials, dict)
    assert len(config.hosts) == 0

    assert Manufacturer.dell in config.default_credentials
    dell_creds = config.default_credentials[Manufacturer.dell]
    assert dell_creds.username == "root"
    assert dell_creds.password.get_secret_value() == "dellpass"


def test_configuration_model_with_hosts():
    config = Configuration(
        hosts=[
            DellServer(
                name="test1",
                url="https://1.2.3.4",
                manufacturer=Manufacturer.dell,
                idrac_version=9,
            ),
            SupermicroServer(
                name="test2",
                url="https://1.2.3.5",
                manufacturer=Manufacturer.supermicro,
            ),
        ],
        default_credentials={
            Manufacturer.dell: Credentials(username="root", password=SecretStr("dellpass")),
            Manufacturer.hpe: Credentials(username="admin", password=SecretStr("hpepass")),
        },
    )

    assert len(config.hosts) == 2
    assert config.hosts[0].name == "test1"
    assert config.hosts[1].name == "test2"

    assert len(config.default_credentials) == 2
    assert all(isinstance(k, Manufacturer) for k in config.default_credentials.keys())
    assert Manufacturer.dell in config.default_credentials
    assert Manufacturer.hpe in config.default_credentials
