# AGENTS

This repository is a Python SDK for interacting with Zyxel NR5103E routers.

## Workflow
- Use the Python version specified in `.python-version`.
- Source files live under `src/` and tests under `tests/`.
- Run `bin/format` to apply ruff autoformatting.
- Run `bin/test` after changes. It performs ruff linting, checks formatting, runs mypy and pytest.
- Update dependencies with `uv sync`; never edit `uv.lock` manually.

Always run both commands before committing code.

## Development Setup
The project configuration and dependencies live in `pyproject.toml`.
Create a virtual environment and install the SDK in editable mode with its
`dev` extras to get the tooling used by `bin/format` and `bin/test`:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e . --group dev
```
