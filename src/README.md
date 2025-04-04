## Build ontology using EMMOntoPy

here is the source code to create the MagneticMaterialsOntology using  
`https://github.com/emmo-repo/EMMOntoPy`  

### Manual Installation and execution

install EMMOntoPy
```
pip install EMMOntoPy
```

clone the MagneticMaterialsOntology
```
git clone git@github.com:MaMMoS-project/MagneticMaterialsOntology.git
```

### Dependences

to create the documentation you need

* pandoc
* Graphviz

### Build or update the ontology

* Change to the directiory `MagneticMaterialsOntology`
* Edit the file `src/build_onto.py`
* Run the command `python src/build_onto.py`  
  This creates the file `magnetic_material_mammos.ttl`
* Run the emmocheck `emmocheck magnetic_material_mammos.ttl`

or simply run
```
./create.sh
```

which builds the ontology, runs the emmocheck and creates a documentation. Please set the relevant path to `emmocheck` and `ontodoc` in the bash script `create.sh`


### Installation and execution using pixi

1. install pixi from https://pixi.sh/

2. clone this repository:

   `git clone https://github.com/MaMMoS-project/MagneticMaterialsOntology.git`

3. Change directory into the cloned repository and run `pixi install`
   to install the required software.

Pixi has predefined tasks (in `pixi.toml`):

- `pixi run build` will create the `magnetic_material_mammos.ttl` file
- `pixi run check` will run `emmocheck`
- `pixi run docs` will build the `doc/magnetic_material_mammos.html`

Alternatively, `pixi shell` can be used to open an environment in
which `emmodoc` and `ontodoc` are in the search path, and the relevant
commands can be executed directly.

Within this environment, `sh create.sh` will carry out all the tasks above
subsequently.

### Strategy

#### Building a magnetic materials ontology

The classes and attributes cover the input and output of the simulation workflow and measurement workflow of the Magnetic Multiscale Modelling Suite (MaMMoS) project. Starting point for creating the ontology are the modelling data (MODA) and characterisation data (CHADA) diagrams of MaMMoS.

#### Elucidation
When possible we use the definition in a text book for the *elucidation*, which is given by the doc string of the python class. 

The following text books have been used 

"Magnetism and Magnetic Materials" by J.M.D Coey, Cambridge University Press, 2009.  
"Magnetism II-Materials and Applications" edited by Étienne du Trémolet Lacheisserie, Damien Gignoux, Michel Schlenker,Springer, 2002.  
"Permanent Magnetism" by Ralph Skomski and J.M.D. Coey, Institute of Physics Publishing, 1999.  
"Introduction to magnetic materials" by B.D. Cullity and C.D. Graham, Introduction to magnetic materials, John Wiley & Sons, Second Edition, 2009. 

#### EMMO compatibility
We use `EMMOntoPy v0.7.2` to describe the magnetic materials ontology. 

We use `emmocheck` to check that ontologies conform to EMMO conventions.

We load `magnetic_material_mammos.ttl` in `Protégé 5.6.4` and run the reasoner `HermiT 1.4.3.456`
