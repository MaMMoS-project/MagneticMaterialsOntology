#!/bin/bash

# paths to emmocheck and ontodoc (from https://github.com/emmo-repo/EMMOntoPy)
CHECK=../onto/emmocheck

echo "remove previous files ..."
rm demo.sqlite3
rm magnetic_material_mammos.ttl

echo "building ontology ..."
python src/build_onto.py
ls -ls magnetic_material_mammos.ttl

echo "checking ontology ..."
$CHECK magnetic_material_mammos.ttl

echo "building documentation ..."
cd doc
./mammosdoc --template=mammos.md --local --format=html ../magnetic_material_mammos.ttl magnetic_material_mammos.html
cd ..
ls -ls doc/magnetic_material_mammos.html
