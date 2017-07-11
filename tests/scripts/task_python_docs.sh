#!/bin/bash
mkdir -p docs/_build/html
rm -rf docs/_build/html/jsdoc
rm -rf docs/_build/html/doxygen
# C++ doc
make doc

# JS doc
jsdoc web/tvm_runtime.js web/README.md || exit -1
mv out docs/_build/html/jsdoc || exit -1
mv docs/doxygen docs/_build/html/doxygen || exit -1

cd docs
PYTHONPATH=../python make html || exit -1
cd _build/html
tar czf docs.tgz *
mv docs.tgz ../../../
