#!/bin/bash

git status

echo "commit to git ..."
git add doc/magnetic_material_mammos.html
git add magnetic_material_mammos.ttl
git add src/build_onto.py
git commit -m "$1"
