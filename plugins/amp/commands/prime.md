## Usage

`/prime <ADDITIONAL_GUIDANCE>`

## Process

Perform all actions below.

Instructions assume you are in the repo root directory, change there if needed before running.

READ (or RE-READ if already READ):
@philosophies/IMPLEMENTATION_PHILOSOPHY.md
@philosophies/MODULAR_DESIGN_PHILOSOPHY.md

RUN:
# Ensure dependencies are installed (no manual venv activation needed)
uv sync

# Run checks and tests using uv (works with or without Makefile)
uv run make check || uv run ruff check . || echo "⚠️ No linter found, skipping"
uv run make test || uv run pytest || echo "⚠️ No tests found, skipping"

## Additional Guidance

$ARGUMENTS
