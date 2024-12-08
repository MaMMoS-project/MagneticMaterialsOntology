#!/bin/bash

# paths to emmocheck and ontodoc (from https://github.com/emmo-repo/EMMOntoPy)
CHECK=../onto/emmocheck
DOC=../onto/ontodoc

echo "remove previous files ..."
rm demo.sqlite3
rm magnetic_material_mammos.ttl

echo "building ontology ..."
python src/build_onto.py
ls -ls magnetic_material_mammos.ttl

echo "checking ontology ..."
$CHECK magnetic_material_mammos.ttl

echo "building documentation ..."
$DOC --format simple-html magnetic_material_mammos.ttl doc/magnetic_material_mammos.html 
ls -ls doc/magnetic_material_mammos.html
