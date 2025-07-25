# GitHub CoPilot Instructions for nr5103e-sdk

## Project Overview

This is a Python SDK for interacting with Zyxel NR5103E routers. The SDK handles login, sessions, and basic router queries with a clean, context-manager based API.

## Development Environment Setup

### Prerequisites
- Python version as specified in `.python-version`
- uv package manager

### Quick Setup
```sh
# Install uv if not already available
pip install uv

# Install dependencies
uv sync

# Verify setup
uv run bin/test
```

## Development Workflow

### Code Formatting
- **Always run** `uv run bin/format` before committing code
- Uses ruff for both linting fixes and code formatting

### Testing
- **Always run** `uv run bin/test` before committing code
- Includes: ruff linting, format checking, mypy type checking, and pytest

### Dependencies
- Use `uv sync` to update dependencies
- **Never** edit `uv.lock` manually - it's managed by uv
- Development dependencies are defined in `pyproject.toml` under `[dependency-groups]`

## Code Style and Conventions

### Linting Configuration
- Uses ruff with "ALL" rules enabled
- Specific ignores in `pyproject.toml`:
  - `COM812`, `D203`, `D213`: Style conflicts
  - `FIX`, `TD`: TODO/FIXME comments allowed
- Test files have relaxed rules (see `pyproject.toml`)

### Type Checking
- Uses mypy for static type analysis
- All code should be properly type-annotated
- Types-* packages provide type stubs for external dependencies

### Testing
- Uses pytest for unit testing
- Test files located in `tests/` directory
- Tests should follow existing patterns in the repository
- Debug logging enabled in pytest configuration

## Project Structure

```
src/nr5103e_sdk/    # Main SDK source code
tests/              # Unit tests
bin/                # Development scripts (format, test)
.github/workflows/  # CI configuration
pyproject.toml      # Project configuration and dependencies
uv.lock            # Locked dependency versions (auto-managed)
```

## API Design Principles

- Use context managers for resource management (see `Client` class)
- Handle authentication and session management internally
- Provide clean, intuitive interfaces for router operations
- Follow Python naming conventions and best practices

## Common Tasks

### Adding New Features
1. Implement in appropriate module under `src/nr5103e_sdk/`
2. Add comprehensive type annotations
3. Write unit tests in `tests/`
4. Run `uv run bin/format` and `uv run bin/test`
5. Ensure all checks pass before committing

### Adding Dependencies
1. Add to `pyproject.toml` under `dependencies` or `[dependency-groups].dev`
2. Run `uv sync` to update lock file
3. For type checking, add corresponding `types-*` package if available

### Debugging
- Tests run with debug logging enabled
- Use pytest's `-v` flag for verbose output
- Leverage the existing test patterns for new functionality

## Important Notes

- This SDK interacts with network devices - be mindful of authentication and security
- All network operations should be properly handled with appropriate error handling
- The Client class uses session management - understand the authentication flow
- Always test with the existing test patterns to maintain consistency
