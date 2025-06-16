#!/bin/bash

# Update package list (fixing typo 'udate' to 'update')
apt update

# Install curl
apt install -y curl

curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

apt install -y nodejs

npm install -g localtunnel


# Uninstall cmake via pip (if installed that way)
pip uninstall -y cmake

# Install cmake via apt
apt install -y cmake

apt install libopenblas-dev liblapack-dev libatlas-base-dev


python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

pip install "numpy<2"
 

