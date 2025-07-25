# GitHub Copilot Instructions for nr5103e-sdk

## Project Overview

Python SDK for interacting with Zyxel NR5103E routers. Handles login, sessions, and basic router queries with a clean, context-manager based API.

## Development Environment Setup

### Prerequisites
- Python version as specified in `.python-version`
- uv package manager

### Quick Setup
```sh
pip install uv  # if not available
uv sync
uv run bin/test
```

## Development Workflow

### Code Formatting & Testing
- **Always run** `uv run bin/format` before committing
- **Always run** `uv run bin/test` before committing
- Includes ruff linting/formatting, mypy type checking, and pytest
- **Update PR descriptions** with test results after addressing feedback

### Dependencies
- Use `uv sync` to update dependencies
- **Never** edit `uv.lock` manually
- Development dependencies defined in `pyproject.toml` under `[dependency-groups]`

### Communication and Progress Tracking
- **Keep PR descriptions current** - primary communication tool with reviewers
- **Update progress frequently** throughout development
- **Be transparent** about challenges, approach changes, or additional scope
- **Use checklists effectively** to track progress and communicate status

## Development Principles

- Make minimal changes to complete tasks fully, without unnecessary complications or premature optimisations
- Simple is better than complex
- Avoid obvious or unhelpful comments; only add comments when code is not idiomatic or when explaining complex logic
- Tests should verify intended functionality, not implementation specifics
- Tests should only require updates when features change or new behaviours need regression testing

## Code Style and Conventions

### File Formatting
- **Always add newline** to end of all text files
- Ensures proper formatting and avoids issues with tools and Git

### Language
- **Always use British English** in all code comments, documentation, and prose

### Linting & Type Checking
- Uses ruff with "ALL" rules enabled (configured in `pyproject.toml`)
- Uses mypy for static type analysis with comprehensive type annotations
- Types-* packages provide type stubs for external dependencies

### Testing
- Uses pytest for unit testing in `tests/` directory
- Debug logging enabled in pytest configuration
- Tests should follow existing patterns

## Project Structure

```
.github/workflows/  # CI configuration
bin/                # Development scripts (format, test)
pyproject.toml      # Project configuration and dependencies
src/nr5103e_sdk/    # Main SDK source code
tests/              # Unit tests
uv.lock            # Locked dependency versions (auto-managed)
```

## API Design Principles

- Use context managers for resource management
- Handle authentication and session management internally
- Provide clean, intuitive interfaces for router operations
- Follow Python naming conventions and best practices

## Common Tasks

### Adding New Features
1. Create initial PR with clear description and checklist
2. Implement in `src/nr5103e_sdk/`
3. Add comprehensive type annotations
4. Write unit tests in `tests/`
5. Update PR description as work progresses
6. Run `uv run bin/format` and `uv run bin/test`
7. Ensure all checks pass before requesting review

### Adding Dependencies
1. Add to `pyproject.toml` under `dependencies` or `[dependency-groups].dev`
2. Run `uv sync` to update lock file
3. Add corresponding `types-*` package if available for type checking

### Debugging
- Tests run with debug logging enabled
- Use pytest's `-v` flag for verbose output
- Leverage existing test patterns for new functionality

## Important Notes

- SDK interacts with network devices - be mindful of authentication and security
- All network operations should have proper error handling
- Client class uses session management - understand authentication flow
- Always test with existing patterns to maintain consistency

## Pull Request Management

### PR Description and Progress Tracking
- **Always update** PR description throughout development lifecycle
- **Update PR descriptions** when:
  - Completing meaningful units of work
  - Changing approach or discovering new requirements
  - Responding to code review feedback
  - Adding or removing scope from original plan
  - Encountering blockers or dependencies
- **Maintain clear checklist** showing completed and pending work

### Code Review Response Workflow
- **When receiving code review feedback:**
  - Update PR description to acknowledge feedback
  - Add new checklist items for addressing review comments
  - Update progress as changes are implemented
  - **Always** run `uv run bin/format` and `uv run bin/test` after changes
  - Mark review items as completed when addressed
- **Keep reviewers informed** with summary of changes, questions, and testing results

### Iterative Development Communication
- Update PR descriptions to reflect current understanding
- Add context about design decisions or trade-offs discovered
- Document changes to original scope or approach
- Keep checklist current - add/modify/remove items as needed
- Before requesting review, ensure PR description accurately reflects completed work

## Documentation Maintenance

### Keeping Documentation Current
- **Always update README.md** when adding new features, changing APIs, or modifying project structure
- **Always update copilot-instructions.md** when project structure, tools, processes, or requirements change
- Update code examples and usage patterns to reflect current API
- Ensure all file paths and command references remain accurate
- **Use British English** in all documentation and prose
