#!/bin/bash

echo $(ruff --config ruff.toml check --select I --fix .)
echo $(ruff --config ruff.toml format --line-length 80 .)
echo $(ruff --config ruff.toml format --line-length 100 ./main_service/infrastructure/tests/integration_tests/)
