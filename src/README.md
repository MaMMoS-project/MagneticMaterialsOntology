## Build ontology using EMMOntoPy

here is the source code to create the MagneticMaterialsOntology using  
`https://github.com/emmo-repo/EMMOntoPy`  

### Installation

install EMMOntoPy
```
pip install EMMOntoPy
```

clone the MagneticMaterialsOntology
```
git clone git@github.com:MaMMoS-project/MagneticMaterialsOntology.git
```

### Build or update the ontology

* Change to the directiory `MagneticMaterialsOntology`
* Edit the file `src/build_onto.py`
* Run the command `python src/build_onto.py`  
  This creates the file `magnetic_material_mammos.ttl`
* Run the emmocheck `emmocheck magnetic_material_mammos.ttl`

