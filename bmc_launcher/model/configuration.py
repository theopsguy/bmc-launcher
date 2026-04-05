from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_serializer


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)


class Credentials(BaseConfigModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None

    @field_serializer("password", mode="plain")
    def mask_password(self, value: Optional[SecretStr]) -> Optional[str]:
        return "**********" if value else None


class Manufacturer(str, Enum):
    dell = "DELL"
    hpe = "HPE"
    supermicro = "SUPERMICRO"


class Server(BaseConfigModel):
    name: str
    url: str
    manufacturer: Manufacturer
    credentials: Optional[Credentials] = None

    @property
    def bmc_version(self) -> Optional[int]:
        return None

    def get_credentials(self, default_credentials: Dict[Manufacturer, Credentials]) -> Credentials:
        if self.credentials:
            if not self.credentials.username or not self.credentials.password:
                raise ValueError(
                    f"Server '{self.name}' has partial credentials: both username and password must be set"
                )
            return self.credentials

        if self.manufacturer not in default_credentials:
            raise ValueError(
                f"Server '{self.name}' has no credentials and no default credentials for {self.manufacturer.value}"
            )

        return default_credentials[self.manufacturer]


class DellServer(Server):
    manufacturer: Literal[Manufacturer.dell]
    idrac_version: int

    @property
    def bmc_version(self) -> int:
        return self.idrac_version


class HPEServer(Server):
    manufacturer: Literal[Manufacturer.hpe]
    ilo_version: int

    @property
    def bmc_version(self) -> int:
        return self.ilo_version


class SupermicroServer(Server):
    manufacturer: Literal[Manufacturer.supermicro]
    pass


ServerType = Annotated[Union[DellServer, HPEServer, SupermicroServer], Field(discriminator="manufacturer")]


class Configuration(BaseConfigModel):
    hosts: List[ServerType] = Field(default_factory=list)
    default_credentials: Dict[Manufacturer, Credentials] = Field(default_factory=dict)
