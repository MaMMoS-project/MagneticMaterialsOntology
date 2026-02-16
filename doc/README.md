## Create documentation 

### Generating html documentation

We use the Python script `mammosdoc-cli.py` which is a modified version of `ontodoc` from EMMOntoPy as follows

* Change to the directory `MagneticMaterialsOntology/doc`
* Run mammosdoc: 

```
python mammosdoc-cli.py --template=mammos.md --local --format=html ../magnetic_material_mammos.ttl magnetic_material_mammos.html  
```
for creating the html file.

### Documentation

The created documentation can be viewed here   
[view html file](https://mammos-project.github.io/MagneticMaterialsOntology/doc/magnetic_material_mammos.html) .

### Change the content of the html file

You may change the content of the html file by editing the following files

#### mammos.md, specify graphs to be shown

Gives the content of the html file. It is a markdown file that will be converted to an html file.
With preprocessing commands, which start with %, content from the ontology can be included.
Examples are:

```
%HEADER "header text" level=2  
creates a header that is included in the table of content

%BRANCHFIG name addnodes=1 parents=0 rankdir='LR' relations=isA,hasSpatialPart,hasSpatialTile edgelabels=1  
adds a plot of the ontology branch `name`
```

You may use the following parameters:
|parameter and default value | task |
|----------------------------|------|  
|caption='' | will add a caption below the graph|
|terminated=1 | whether the graph should be terminated at leaf nodes|
|strict_leaves=1 | whether to strictly exclude leave descendants|
|width=0px | optional figure width|
|leaves='' | optional leaf node names for graph termination|
|relations='all' | comma-separated list of relations to include|
|edgelabels=0 | whether to include edgelabels|
|rankdir='BT' | graph direction (BT, TB, RL, LR: bottom-top, top-bottom, right-left, left-right)|
|legend=1 | whether to add legend|
|namespaces='' | sequence of names of namespaces to be included|
|ontologies='' | sequence of names of ontologies to be included|
|addnodes=1 | whether to add missing target nodes in relations (1: True, 0: False)|
|parents=1 | Adds n levels of parents to graph|

#### pandoc-options.yaml 

`mammosdoc` or `ontodoc` use pandoc to generate the documentation.

Provide pandoc arguments/options via this file. These include the name of the input file for the meta data, the depth of the table of content, and the filename of the files for logo and EU flag.

#### pandoc-html-options.yaml

Provide pandoc arguments for html output via this file. These include the html style file and the html template.

#### pandoc-template.html, pandoc-html.css

The html template file and html style file.

### Create a plot of a concept

Here is an example for plotting branches. To create on or more plots you can use `mammosdoc`. 

* Add multiple BRANCHFIG preprocessing directives to the markdown template file `plots.md` 
* Change to the directory `MagneticMaterialsOntology/doc`
* Run mammosdoc: 

```
python mammosdoc-cli.py --template=plots.md --local --format=html ../magnetic_material_mammos.ttl plots.html  
```
will create a html file with the plots. The plots are also stored in the directory `genfigs` as scalable vector graphic (svg) file.

The parameters after the preprocessor directive `%BRANCHFIG` in the file `plots.md` define what is plotted for a branch. Here are a few tips.

| problem | solution | parameter setting |
|---------|----------|-------------------|
| no children are displayed | add missing target nodes in relations | `addnodes=1` |
| plot has too many nodes | reduce level of shown parents | `parents=0` | 
| plot has too many connection | select only a few relations | `relations=isA,hasSpatialPart` | 
| bubbles and fonts are very small | change graph direction | `rankdir='LR'` |

For readability it is recommended to switch on edge labels with `edgelabels=1` and to add a caption with `caption='Explain what we see.'`

[view the plots](https://mammos-project.github.io/MagneticMaterialsOntology/doc/plots.html)

