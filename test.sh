#!/bin/bash

set -e

cd tests

if [ ! -d build ]; then
  mkdir build
fi

cd build
cmake ..
cmake --build . --target all
ctest
