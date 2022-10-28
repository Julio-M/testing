#!/bin/bash
set -e
######### CONSTANTS #############################
BASE_DIR=$(pwd)
VENV_NAME="env"

function health() {
    echo "I am reachable"
    echo "$(whoami)"
}

function activateEnv(){
    echo "--> Checking for virutalenviroment <-----"
    if [[ -e "${VENV_NAME}" ]]; then
        echo "---Enviroment exists---"
    else
        echo ">-Creating new enviroment-<"
        python3 -m venv "${VENV_NAME}"
        echo ">-Done-<"
    fi
    VENV_DIR="${BASE_DIR}/${VENV_NAME}"
    VENV_EXECUTABLE="${VENV_DIR}/bin/activate"
    moduleBasePath="."
    echo "--> Activating virutalenviroment ${VENV_NAME}<-----"
    source "${VENV_EXECUTABLE}"
    pip install -U pip &&
    echo "Using $(which python)" &&
    pip install -r "${moduleBasePath}"/requirements.txt
}

function runLocally() {
    activateEnv ${VENV_NAME} &&
    clear && python main.py
}

function deleteEnv(){
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "delete_venv needs ${N} parameter(s)"
        exit 1
    fi
    moduleName=$1
    VENV_NAME="${moduleName}"
    if [[ -e "${VENV_NAME}" ]]; then
        echo "---Enviroment found---"
        echo "---Deleting---"
        rm -rf "${VENV_NAME}"
    else
        echo "---No venv set---"
    fi
}

function cleanup(){
    rm -rf ./__pycache__
    deleteEnv ${VENV_NAME}
}