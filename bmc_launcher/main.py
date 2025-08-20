import argparse
import logging
import sys
from io import StringIO
from os.path import expanduser

from ruamel.yaml import YAML

from bmc_launcher.configuration import Configuration
from bmc_launcher.launchers.factory import SeleniumFactory
from bmc_launcher.web_drivers.factory import WebDriverFactory

log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", type=str, help="Host IP address or hostname")
    parser.add_argument("-l", "--list-hosts", action="store_true", help="List all available hosts")
    parser.add_argument(
        "-d", "--driver", type=str, choices=["chrome"], default="chrome", help="Web driver to use (default: chrome)"
    )
    parser.add_argument("-i", "--ignore-cert-errors", action="store_true", help="Ignore SSL certificate errors")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=expanduser("~/.bmc_launcher/config.yaml"),
        help="Path to the configuration file",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def setup_logging(verbose: bool):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def list_hosts(config: Configuration):
    if not config.hosts:
        log.info("No hosts defined in the configuration.")
        return

    hosts_data = [host.model_dump() for host in config.hosts]

    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    stream = StringIO()
    yaml.dump(hosts_data, stream)

    print(stream.getvalue())


def main():
    args = parse_args()
    setup_logging(args.verbose)

    try:
        config = Configuration(config_path=args.config)
    except FileNotFoundError:
        log.error(f"Configuration file not found at {args.config}")
        sys.exit(1)
    except Exception:
        log.exception("Unexpected error while loading configuration:")
        sys.exit(1)

    if args.list_hosts:
        list_hosts(config)
        return

    if not args.host:
        log.error("You must specify a host with -H or use -l to list hosts.")
        sys.exit(1)

    host = config.get_host_by_name(args.host)
    if not host:
        log.error(f"Host '{args.host}' not found in configuration.")
        sys.exit(1)

    credentials = host.get_credentials(config.default_credentials)
    if not credentials:
        log.error(f"No credentials found for host '{args.host}'.")
        sys.exit(1)
    host.credentials = credentials

    driver = WebDriverFactory(args.driver, args.ignore_cert_errors)
    selenium_controller = SeleniumFactory(host, driver.get_webdriver())
    selenium_controller.launch()


if __name__ == "__main__":
    main()
