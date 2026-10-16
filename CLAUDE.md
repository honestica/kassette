# Kassette

Kubernetes snapshot testing tool (inspired by Ruby VCR): records `kubectl get` output as YAML "kassettes" and diffs them against the live cluster state.

Published on PyPI as `kassette-k8s`; the Python package and the CLI command are both named `kassette`.

The GitHub repository is **public**: anyone can open a PR from a fork, so never put internal names, hostnames, cluster data or secrets in the code, tests, examples or snapshots.

## Layout

- `src/kassette/`: the package (`__init__.py` holds the CLI entry point `run()`)
- `tests/`: unit tests (`unittest` style, run with pytest) and `e2e.yaml`, the resources deployed by the end-to-end test
- `examples/`: sample kassette configurations (`examples/demo` doubles as the end-to-end reference, see below)
- `bin/`: dev scripts (`test`, `lint`, `fmt`, `e2e`, `publish`)

## Commands

The package must be installed in the active environment (`pipenv run pip install -e .`), then:

```bash
pipenv sync --dev
pipenv run bin/test    # pytest
pipenv run bin/lint    # flake8, mypy (strict), isort, black --check
pipenv run bin/fmt     # isort + black
pipenv run bin/e2e     # end-to-end test, see below
```

## End-to-end test

`bin/e2e` is local only (not run in CI). It needs `docker`, `kind` and `kubectl`, and creates a disposable kind cluster with a temporary kubeconfig, deployed from `tests/e2e.yaml`. It then checks that:

- `kassette record demo` leaves the committed `examples/demo` files unchanged
- `kassette diff demo` exits with 0 on the unchanged cluster
- `kassette diff demo` exits with 1 once the Deployment replicas are changed

Never run it against an existing cluster, and ask before running it: it starts Docker containers. If `record` changes `examples/demo`, review the diff before committing the new kassettes.

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
- Releases: bump `version` in `pyproject.toml`, merge to `master`, then push the tag `vX.Y.Z` (it must match the version). `release.yaml` publishes to PyPI through Trusted Publishing, after approval on the `pypi` environment. Never push a release tag without being asked
- Every push to `master` touching `src/**`, `pyproject.toml` or `README.md` publishes a `.devN` version to TestPyPI (`publish-test.yaml`)
