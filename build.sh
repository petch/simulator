#!/bin/bash

python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ -u petch -p testredmonster dist/*

rm -rf build
rm -rf dist
rm -rf *.egg-info

python3 -m pip install --upgrade --no-cache-dir --index-url https://test.pypi.org/simple/ --no-deps navierstokes-petch
