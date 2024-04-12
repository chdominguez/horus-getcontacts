#!/bin/bash

echo "This plugin needs several software to be installed in your computer in order to work"

echo "Assuming conda is intalled..."

# Find if conda is installed
command="conda"
if ! command -v $command &> /dev/null; then
    echo "Error: Command '$command' not found" >&2
    echo "Trying micromamba...."
    command="micromamba"
    if ! command -v $command &> /dev/null; then
        echo "Error: Command '$command' not found, exiting..." >&2
        exit 1
    fi

    # Init micromamba
    eval "$(micromamba shell hook --shell bash)"
else
    # Init conda
    eval "$(conda shell.bash hook)"
fi

echo "Installing environment..."

# Create conda environment for plugin
yes | $command create -n nostrum_internal_plugin

$command activate nostrum_internal_plugin

# Check if the system is macOS
# if [ "$(uname -s)" -eq "Darwin" ]; then
#     yes | brew install netcdf # Assumes https://brew.sh/ is installed
# fi

# Install dependencies
yes | $command install -c conda-forge python=3.9 numpy scipy expat matplotlib scikit-learn pytest pandas seaborn cython tk=8.6 vmd-python libnetcdf