# Review and test code changes

Everything below assumes you are in the repo root directory, change there if needed before running.

RUN:
# Install dependencies and run checks (works with or without Makefile)
uv sync  # Ensure dependencies are installed

# Run linting/formatting checks
uv run ruff check . || uv run make check || echo "⚠️ No linter found, skipping"

# Run tests
uv run pytest || uv run make test || echo "⚠️ No tests found, skipping"

If all tests pass, let's take a look at the implementation philosophy documents to ensure we are aligned with the project's design principles.

READ:
@philosophies/IMPLEMENTATION_PHILOSOPHY.md
@philosophies/MODULAR_DESIGN_PHILOSOPHY.md

Now go and look at what code is currently changed since the last commit. Ultrathink and review each of those files more thoroughly and make sure they are aligned with the implementation philosophy documents. Follow the breadcrumbs in the files to their dependencies or files they are importing and make sure those are also aligned with the implementation philosophy documents.

Give me a comprehensive report on how well the current code aligns with the implementation philosophy documents. If there are any discrepancies or areas for improvement, please outline them clearly with suggested changes or refactoring ideas.

## Additional Guidance

$ARGUMENTS
