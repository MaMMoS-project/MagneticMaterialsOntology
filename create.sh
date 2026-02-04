#!/bin/bash


# paths to emmocheck and ontodoc (from https://github.com/emmo-repo/EMMOntoPy)
CHECK=emmocheck

echo "remove previous files ..."
rm -f magneticmaterials.sqlite3
rm -f magnetic_materials_ontology_mammos.ttl

echo "building ontology ..."
python src/build_onto.py
ls -ls magnetic_materials_ontology_mammos.ttl
echo "checking ontology ..."
$CHECK magnetic_materials_ontology_mammos.ttl


# on ARM Mac, this seems required once to build documentation
doc -c

echo "building documentation ..."
cd doc
python ./mammosdoc --template=mammos.md --local --format=html ../magnetic_materials_ontology_mammos.ttl magnetic_materials_ontology_mammos.html
cd ..
ls -ls doc/magnetic_materials_ontology_mammos.html
