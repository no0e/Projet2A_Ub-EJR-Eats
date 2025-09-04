#!/bin/sh

# Install the package managers
pip install --user pdm uv

# PDM configuration
pdm config use_uv true

# Setup VSCode extensions
code-server --install-extension charliermarsh.ruff meta.pyrefly
code-server --uninstall-extension ms-python.flake8