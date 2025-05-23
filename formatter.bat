@echo off
echo Running ruff check with autofix...
ruff --config ruff.toml check --select I --fix .
echo.

echo Running ruff format...
ruff --config ruff.toml format --line-length 80 .
echo.

echo Done.