# kassette
Another kubernetes testing tools

It takes inspiration from ruby https://github.com/vcr/vcr applied to kubernetes resources for testing purposes.

## Features

- take a yaml snapshot of the defined (from global configuration `kassette.yaml` and the ones from `examples` folder) kubernetes resource cluster and save it:
    `kassette record`
- compare the recorded yaml snapshot with the current kubernetes cluster state:
    `kassette diff`
- you can also do mass modification of all the resources in the snapshot with `kassette modify` command

# Installation

```bash
pip install kassette-k8s
```

The package is named `kassette-k8s`, but the installed command is `kassette`.

# Usage

For usage details, see: `kassette [COMMAND] --help`

`kassette` reads `kassette.yaml` and the `examples` folder from the current directory.

# Requirements

This tools require the `kubectl` cli, it will use exclusively the `get` subcommand to retrieve the kubernetes resources.

Requires python 3.10+ (tested with python 3.12).

# Contribution

Requires pipenv.

```bash
pipenv sync --dev
pipenv run pip install -e .
pipenv run bin/test
pipenv run bin/lint
```

# Next steps
- use CI to run tests and linting
