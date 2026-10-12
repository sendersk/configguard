# ConfigGuard

ConfigGuard is a Python CLI tool for validating application configuration files before deployment. It supports YAML and JSON, validates configuration data using Pydantic models, and provides human-readable or JSON output.

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Ruff](https://img.shields.io/badge/linted%20with-Ruff-D7FF64?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)



## Features

- Load configuration files in YAML, YML, and JSON formats.
- Validate required fields, data types, and configuration constraints.
- Check cross-field rules, including production environment restrictions.
- Enable additional validation rules with strict mode.
- Display validation results in human-readable or JSON format.
- Return meaningful exit codes for automation and CI/CD workflows.
- Use structured logging for troubleshooting.

## Requirements

- Python 3.13 or newer
- uv

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/sendersk/configguard.git
cd configguard
```

Install the project and its dependencies:

```bash
uv sync
```

## Usage

Display help:

```bash
uv run configguard --help
```

Display the installed version:

```bash
uv run configguard --version
```

Validate a configuration file:

```bash
uv run configguard resources/valid.yaml
```

Use JSON output:

```bash
uv run configguard resources/valid.json --format json
```

Enable strict validation:

```bash
uv run configguard resources/valid.yaml --strict
```

Strict mode applies additional rules. For example, production configurations must specify a database password when strict validation is enabled.

## Supported formats

ConfigGuard supports `.yaml`, `.yml`, and `.json` configuration files. The configuration file must contain a mapping at its root.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Configuration is valid |
| `1` | Configuration validation failed |
| `2` | Input or command usage error |

These exit codes allow ConfigGuard to be used in scripts and CI/CD pipelines.

## Development

Run the test suite:

```bash
uv run pytest
```

Check code style:

```bash
uv run ruff check .
```

Run static type checking:

```bash
uv run mypy src
```

## Project status

ConfigGuard is a portfolio project focused on Python development, configuration validation, automated testing, CLI design, and maintainable code.