from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_serializer, field_validator
from typing import List, Optional, Union, Dict, Annotated, Literal
from enum import Enum


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


class Server(BaseModel):
    name: str
    url: str
    manufacturer: Manufacturer
    credentials: Optional[Credentials] = None

    class Config:
        use_enum_values = True

    def get_credentials(self, default_credentials: Dict[Manufacturer, Credentials]) -> Credentials:
        if self.credentials and self.credentials.username and self.credentials.password:
            return self.credentials
        return default_credentials.get(self.manufacturer, Credentials())


class DellServer(Server):
    manufacturer: Literal[Manufacturer.dell]
    idrac_version: int


class HPEServer(Server):
    manufacturer: Literal[Manufacturer.hpe]
    ilo_version: int


class SupermicroServer(Server):
    manufacturer: Literal[Manufacturer.supermicro]
    pass


ServerType = Annotated[Union[DellServer, HPEServer, SupermicroServer], Field(discriminator="manufacturer")]


class Configuration(BaseConfigModel):
    hosts: List[ServerType] = Field(default_factory=list)
    default_credentials: Dict[Manufacturer, Credentials] = Field(default_factory=dict)
