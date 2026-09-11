# BMC Launcher

A command-line utility that uses Selenium WebDriver to launch a browser, navigate to a server's BMC (Baseboard Management Controller) web interface, and login automatically.

## Installation

Install with [pipx](https://pipx.pypa.io/stable/how-to/install-pipx.html) (recommended). This installs `bmc-launcher` in an isolated environment and puts it on your `PATH`:

```
pipx install bmc-launcher
```

Alternatively, install with pip:

```
pip3 install bmc-launcher
```

### Development setup

1. Clone the repository
    ```
    git clone https://github.com/theopsguy/bmc-launcher.git
    cd bmc-launcher
    ```

1. Install dependencies with [Poetry](https://python-poetry.org/):
    ```
    pip3 install poetry && poetry install
    ```

1. Run the tool via Poetry:
    ```
    poetry run bmc-launcher -l
    ```

## Configuration

### Default location:

`~/.bmc_launcher/config.yaml`

### Example

```yaml
default_credentials:
  hpe:
    username: admin
    password: mysecret
  dell:
    username: root
    password: dellpass

hosts:
  - name: web00
    url: https://192.168.1.10
    manufacturer: hpe
    ilo_version: 4
  - name: db00
    url: https://192.168.1.11
    manufacturer: dell
    idrac_version: 9
    credentials:
      username: specialuser
      password: otherpass
```

- `HPE` hosts require `ilo_version`
- `DELL` hosts require `idrac_version`
- `SUPERMICRO` hosts need neither. 

Currently supported versions are iLO 4 and iDRAC 8/9.

## Usage

- List hosts defined in the configuration:

```
% bmc-launcher -l
  - name: web00
    url: https://192.168.1.10
    manufacturer: HPE
    credentials:
      username: Administrator
      password: '**********'
    ilo_version: 4
  - name: firewall00
    url: https://192.168.1.1
    manufacturer: SUPERMICRO
    credentials:
  - name: test_dell
    url: https://10.0.0.1
    manufacturer: DELL
    credentials:
    idrac_version: 9
```

- Launch BMC:

```
bmc-launcher -H web00 -i
```

### Options

| Flag | Description |
| --- | --- |
| `-H`, `--host` | Host name to launch, as defined in the configuration |
| `-l`, `--list-hosts` | List all available hosts |
| `-d`, `--driver` | Web driver to use (default: `chrome`) |
| `-i`, `--ignore-cert-errors` | Ignore SSL certificate errors |
| `-c`, `--config` | Path to the configuration file (default: `~/.bmc_launcher/config.yaml`) |
| `-v`, `--verbose` | Enable verbose logging |

## Roadmap

- Support loading hosts from an Ansible dynamic inventory, as an alternative to the static `config.yaml` file.

For other ideas or in-progress work, see the [GitHub issues](https://github.com/theopsguy/bmc-launcher/issues).
