# Kassette

Kubernetes snapshot testing tool (inspired by Ruby VCR): records `kubectl get` output as YAML "kassettes" and diffs them against the live cluster state.

Published on PyPI as `kassette-k8s`; the Python package and the CLI command are both named `kassette`.

The GitHub repository is **public**: anyone can open a PR from a fork, so never put internal names, hostnames, cluster data or secrets in the code, tests, examples or snapshots.

## Layout

- `src/kassette/`: the package (`__init__.py` holds the CLI entry point `run()`)
- `tests/`: unit tests (`unittest` style, run with pytest)
- `examples/`: sample kassette configurations
- `bin/`: dev scripts (`test`, `lint`, `fmt`)

## Commands

The package must be installed in the active environment (`pipenv run pip install -e .`), then:

```bash
pipenv sync --dev
pipenv run bin/test    # pytest
pipenv run bin/lint    # flake8, mypy (strict), isort, black --check
pipenv run bin/fmt     # isort + black
```

## Conventions

- Use absolute imports (`from kassette.config import Config`), never flat ones
- Code must pass `bin/lint` (mypy strict: all functions are fully typed)
- Add or update tests for every change
- Code, commits and documentation are written in English
- Never commit secrets
- GitHub Actions are pinned by commit SHA with the version in a trailing comment (`uses: owner/action@<sha> # vX.Y.Z`), never by tag; Dependabot keeps them up to date
- Workflows declare minimal `permissions` and never use `pull_request_target`

## Packaging

- Build metadata lives in `pyproject.toml` (setuptools, `src/` layout)
- The license is declared as an SPDX expression: do not add a `License ::` classifier, setuptools rejects it
- Check a build with `python -m build` then `twine check dist/*`
