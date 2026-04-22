# Magnetic Materials Ontology (MagMO)

Ontology for magnetic materials
===============================
An EMMO-based ontology for magnetic materials.

Status
------

- [X] Proposal
- [ ] Accepted, under development
- [ ] Official

This ontology is work-in-progress (WIP).

* Application submitted: December 2024
* Application accepted on: TBD


Imported ontologies
-------------------

This ontology builds on top of [EMMO](https://github.com/emmo-repo/EMMO) [^1]. See the following table for version
compatibilities:

| Imported Ontologies                       | Version        |                                      |
|-------------------------------------------|----------------|--------------------------------------|
| [EMMO](https://github.com/emmo-repo/EMMO) | 1.0.3 inferred | https://w3id.org/emmo/1.0.3/inferred |


Update ontology version
-----------------------

This repository contains the development of the [EMMO-based repository](https://github.com/emmo-repo/domain-magnetic-materials).

This section shows how to update the ontology to a new version `X.Y.Z` and how to push changes to the EMMO-based repository.

### Update all necessary files in the development repo

1. Let us assume all changes are already merged into branch `main`
2. Update the version string in [`src/build_onto.py`_](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/src/build_onto.py)
3. Update the [`pixi.toml`](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/pixi.toml)
4. Update the [`README.md`](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/README.md) if the EMMO version has changed.
5. Update the [catalog](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/catalog-v001.xml) with the new version number.
6. Update the [contributors turtle file](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/catalog-v001.xml) with the new version number.
7. Update the [dependencies turtle file](https://github.com/MaMMoS-project/MagneticMaterialsOntology/blob/main/magnetic-materials-dependencies.ttl) with the new version number and the dependencies if necessary.
8. Create and push the tag `vX.Y.Z`

### Push the new version onto the EMMO-based repository
Domain ontology repository: https://github.com/emmo-repo/domain-magnetic-materials
1. Start a development branch `X.Y.Z` (See the [EMMO Branching model](https://github.com/emmo-repo/.github/wiki/DomainOntologiesBestPractices#branching-model)).
2. Download the turtle files from the [MagneticMaterialsOntology Releases](https://github.com/MaMMoS-project/MagneticMaterialsOntology/releases) and put them in the `domain-magnetic-materials` repository (overwriting the previous files).
3. Revert namespace changes (work in progress to automate this step).
4. Revert deletion of `dcterms`, `vann`, `bibo` information (work in progress to automate this step).
5. adapt `imports`, `versionIRI`, `versionInfo`.
6. cleanup (work in progress to automate this step).
7. Push all changes to branch `X.Y.Z`.
8. Merge branch `X.Y.Z` to main and delete it.
9. Do a manual GitHub Release.


Using
-----

You may view the ontology by browsing through the [html documentation](https://mammos-project.github.io/MagneticMaterialsOntology/doc/magnetic-materials.html).

Alternatively you can use [Protégé](https://protege.stanford.edu/):
* Install Protégé
* Download the file `magnetic-materials.ttl`  
  Click on the file  
  Select the icon for `Downloading raw file` 
* Start Protégé and open the magnetic materials ontology
  File --> Open `magnetic-materials.ttl`
* Run the Reasoner  
  Reasoner --> select HermiT  
  Reasoner --> Start reasoner 
* Navigate  
  Open the Classes Tab (Window --> Tab: select Classes)  
  Select Inferred at the top right pull down menu of the Classes Tab  
  Use Ctrl-F (Edit --> Find) to search for a term for example type "Magnet"
* Visualize the knowledge tree  
  Open the OntoGraf Tab (Window --> Tab: select OntoGraf)  
  Select an entity in the Classes Tab to visualize
* Reset view (if something goes wrong)  
  Window --> Reset selected tab to default state
  
Building
--------

MagneticMaterialsOntology is built using tools provided by EMMO. For more details see the [src directory](https://github.com/MaMMoS-project/MagneticMaterialsOntology/tree/main/src).

Installation of required software is also explained in  [src/README.md](https://github.com/MaMMoS-project/MagneticMaterialsOntology/tree/main/src/README.md).


Build Status
------------

[![build](https://github.com/MaMMoS-project/MagneticMaterialsOntology/actions/workflows/build.yaml/badge.svg)](https://github.com/MaMMoS-project/MagneticMaterialsOntology/actions/workflows/build.yaml)


Attributions and credits
------------------------

### Authors
- Thomas Schrefl, DISS-UWK
- Wilfried Hortschitz, DISS-UWK

### Projects
- Created within the EU project [MaMMoS](https://mammos-project.github.io/) [^2]. Grant number 101135546 (HORIZON-CL4-2023-DIGITAL-EMERGING-01).

![image info](img/mammos.png)

### Acknowledgement

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or European Health and Digital Executive Agency (HADEA). Neither the European Union nor the granting authority can be held responsible for them.

![image info](img/euflag.png)

License
-------

This project is licensed under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

References
----------

[^1]: https://github.com/emmo-repo/EMMO  
[^2]: https://mammos-project.github.io/
