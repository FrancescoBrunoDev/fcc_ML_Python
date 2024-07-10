#!/bin/bash

# update packages and install build-essential and libhdf5-dev
apt-get update && apt-get install -y build-essential libhdf5-dev

# install python libraries
pip install tensorflow numpy matplotlib pandas scipy scikit-learn