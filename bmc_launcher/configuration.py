import logging
import sys
from pathlib import Path

from pydantic import ValidationError
from ruamel.yaml import YAML

from bmc_launcher.model.configuration import Configuration as ConfigurationModel

log = logging.getLogger(__name__)


class Configuration:
    def __init__(self, config_path: str):
        if not self.is_file(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        config_yaml = self._load(config_path)
        try:
            self.store = ConfigurationModel(**config_yaml)
        except ValidationError as e:
            log.error(f"Configuration validation error: {e}")
            sys.exit(1)

    def _load(self, config_path: str) -> dict:
        log.debug("Loading configuration from %s", config_path)
        with open(config_path, "r") as file:
            data = YAML(typ="safe").load(file)
            if not data:
                raise ValueError(f"Configuration file '{config_path}' is empty or invalid.")

            return self._normalize(data)

    @staticmethod
    def is_file(file_path: str) -> bool:
        return Path(file_path).is_file()

    @staticmethod
    def _normalize(data: dict) -> dict:
        if "default_credentials" in data:
            data["default_credentials"] = {k.upper(): v for k, v in data["default_credentials"].items()}
        for host in data.get("hosts", []):
            if isinstance(host, dict) and "manufacturer" in host:
                host["manufacturer"] = host["manufacturer"].upper()
        return data

    def get_host_by_name(self, name: str):
        return next((h for h in self.hosts if h.name == name), None)

    def __getattr__(self, key):
        if hasattr(self.store, key):
            return getattr(self.store, key)
        raise AttributeError(f"Configuration has no attribute '{key}'")
