# BMC Launcher

A command-line utility that uses Selenium WebDriver to launch a browser, navigate to a server's BMC (Baseboard Management Controller) web interface, and login automatically.

## Installation

1. Create a virtualenv (recommended)
    ```
    python3 -m venv ~/bmc_launcher && source ~/bmc_launcher/bin/activate
    ```

1. Clone the repository
    ```
    git clone https://github.com/pritpal-sabharwal/bmc-launcher.git
    cd bmc-launcher
    ```

1. Install dependencies and utility:
    ```
    pip3 install poetry && poetry install
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

servers:
  - name: web00
    ip: 192.168.1.10
    manufacturer: HPE
  - name: db00
    ip: 192.168.1.11
    manufacturer: dell
    credentials:
      username: specialuser
      password: otherpass
```

## Usage

- List hosts defined in the configuration:

```
% python3 bmc_launcher/main.py -l
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
python3 bmc_launcher/main.py -H web00 -i
```

Note, `-i` disables certificate validation.
