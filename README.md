# kassette
Another kubernetes testing tools

It takes inspiration from ruby https://github.com/vcr/vcr applied to kubernetes resources for testing purposes.

## Features

- take a yaml snapshot of the defined (from global configuration `kassette.yaml` and the ones from `examples` folder) kubernetes resource cluster and save it:
    `bin/kassette record`
- compare the recorded yaml snapshot with the current kubernetes cluster state:
    `bin/kassette diff`
- you can also do mass modification of all the resources in the snapshot with `bin/kassette modify` command

# Usage

For usage details, see: `bin/kassette [COMMAND] --help`

# Requirements

This tools require the `kubectl` cli, it will use exclusively the `get` subcommand to retrieve the kubernetes resources.

Tested with python 3.12, but should work with python 3.10+.

# Contribution

Requires pipenv.

```bash
pipenv sync
pipenv run bin/test
pipenv run bin/lint
```

# Next steps
- use CI to run tests and linting
- publish to pypi
