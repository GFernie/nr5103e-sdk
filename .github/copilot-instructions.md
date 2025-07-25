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
- **Update PR descriptions** with test results, especially after addressing code review feedback

### Dependencies
- Use `uv sync` to update dependencies
- **Never** edit `uv.lock` manually - it's managed by uv
- Development dependencies are defined in `pyproject.toml` under `[dependency-groups]`

### Communication and Progress Tracking
- **Keep PR descriptions current** - they are the primary communication tool with reviewers
- **Update progress frequently** - don't wait until the end to update descriptions
- **Be transparent** about challenges, changes in approach, or additional scope discovered
- **Use checklists effectively** - they help track progress and communicate status clearly

## Development Principles

- Make the minimal amount of changes to complete the task fully, without adding unnecessary complications or premature optimisations.
- Simple is better than complex.
- Only add comments when the code is not idiomatic. The first preference should always be writing code which is self explanatory without comments.
- Tests should test intended functionality rather than just testing the specifics of the implementation. Tests should not require updates when making trivial changes to logic, only when new features are added or behaviours change in a way that we want to test for regressions in the future.

## Code Style and Conventions

### File Formatting
- **Always add a newline** to the end of all text files (source code, configuration files, documentation, etc.)
- This ensures proper file formatting and avoids issues with some tools and Git

### Linting Configuration
- Uses ruff with "ALL" rules enabled
- Specific ignores and rules configured in `pyproject.toml`
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
.github/workflows/  # CI configuration
bin/                # Development scripts (format, test)
pyproject.toml      # Project configuration and dependencies
src/nr5103e_sdk/    # Main SDK source code
tests/              # Unit tests
uv.lock            # Locked dependency versions (auto-managed)
```

## API Design Principles

- Use context managers for resource management (see `Client` class)
- Handle authentication and session management internally
- Provide clean, intuitive interfaces for router operations
- Follow Python naming conventions and best practices

## Common Tasks

### Adding New Features
1. **Create initial PR** with clear description and checklist of planned work
2. Implement in appropriate module under `src/nr5103e_sdk/`
3. Add comprehensive type annotations
4. Write unit tests in `tests/`
5. **Update PR description** as work progresses - check off completed items
6. Run `uv run bin/format` and `uv run bin/test`
7. **Update PR description** with test results and final status
8. Ensure all checks pass before requesting review

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

## Pull Request Management

### PR Description and Progress Tracking
- **Always update** the PR description throughout the development lifecycle, not just at the initial plan
- **Update PR descriptions** when:
  - Completing meaningful units of work (check off completed tasks)
  - Changing approach or discovering new requirements
  - Responding to code review feedback
  - Adding or removing scope from the original plan
  - Encountering blockers or dependencies
- **Maintain a clear checklist** in PR descriptions showing:
  - [x] Completed items with checkmarks
  - [ ] Remaining work with clear descriptions
  - Current status and any blockers
  - Links to related issues or dependencies

### Code Review Response Workflow
- **When receiving code review feedback:**
  - Update the PR description to acknowledge the feedback
  - Add new checklist items for addressing review comments
  - Update progress as you implement suggested changes
  - **Always** run `uv run bin/format` and `uv run bin/test` after making changes
  - Mark review items as completed in the PR description when addressed
- **Keep reviewers informed** by updating the PR description with:
  - Summary of changes made in response to feedback
  - Any questions or clarifications needed
  - Testing results after implementing changes

### Iterative Development Communication
- **Throughout development:**
  - Update PR descriptions to reflect current understanding of the problem
  - Add context about design decisions or trade-offs discovered
  - Document any changes to the original scope or approach
  - Keep the checklist current - add new items as they're discovered
  - Remove or modify items that are no longer relevant
- **Before requesting review:**
  - Ensure PR description accurately reflects all work completed
  - Include testing evidence and verification steps
  - Highlight any areas where reviewer input is specifically needed

## Documentation Maintenance

### Keeping Documentation Up to Date
- **Always update** the README.md when adding new features, changing APIs, or modifying project structure
- **Always update** this copilot-instructions.md file when:
  - Project structure changes (new directories, moved files, etc.)
  - New development tools or processes are added
  - Build/test procedures change
  - New dependencies or requirements are introduced
- Update code examples and usage patterns in documentation to reflect current API
- Ensure all file paths and command references in documentation remain accurate
