#!/bin/bash

echo "This plugin needs several software to be installed in your computer in order to work"

echo "Assuming conda is intalled..."

dependencies="python=3.9 numpy scipy expat matplotlib scikit-learn pytest pandas seaborn cython tk=8.6 vmd-python libnetcdf"

# Find if conda is installed
command="conda"
if ! command -v $command &> /dev/null; then
    echo "Error: Command '$command' not found" >&2
    echo "Trying micromamba...."
    command="micromamba"
    if ! command -v $command &> /dev/null; then
        echo "==============ERROR==============="
        echo "Neither conda or micromamba found" >&2
        echo "You will need to install the "nostrum_internal_plugin" environment manually:"
         echo "conda create -n nostrum_internal_plugin"
        echo "conda activate nostrum_internal_plugin"
        echo "conda install -c conda-forge $dependencies"
        echo "=================================="
        exit 0
    fi

    # Init micromamba
    eval "$(micromamba shell hook --shell bash)"
else
    # Init conda
    eval "$(conda shell.bash hook)"
fi


if { $command env list | grep 'nostrum_internal_plugin'; } >/dev/null 2>&1; then
    echo "Environment already exists..."
    $command env list | grep 'nostrum_internal_plugin'
else
    echo "Installing environment..."

    # Create conda environment for plugin
    yes | $command create -n nostrum_internal_plugin

    $command activate nostrum_internal_plugin

    # Check if the system is macOS
    # if [ "$(uname -s)" -eq "Darwin" ]; then
    #     yes | brew install netcdf # Assumes https://brew.sh/ is installed
    # fi

    # Install dependencies
    yes | $command install -c conda-forge $dependencies
fi