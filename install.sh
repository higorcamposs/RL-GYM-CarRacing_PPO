#!/bin/bash

rm -rf venv/

python -m venv venv

source venv/bin/activate

REQUIREMENTS_FILE="requirements.txt"

pip install --upgrade pip
pip install -r $REQUIREMENTS_FILE

echo "--------------------------------------"
echo "Instalação concluída com sucesso!"
echo "Para usar o ambiente, rode: source venv/bin/activate"
echo "--------------------------------------"
