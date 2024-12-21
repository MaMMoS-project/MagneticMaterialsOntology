%% %% This file %% This is Markdown file, except of lines starting with %% will %% be stripped off. %%

%HEADER Overview 

The MaMMoS magnetic materials ontology is a domain ontology which uses [EMMO](https://github.com/emmo-repo/EMMO) as top level ontology. The magnetic material ontology reflects the hierarchical structure of the magnet. It reveals its physical parts at different length scales.

%HEADER "Magnet" level=2  

A magnet is *functionally defined material*. Possible subclasses of a magnet are *bulk magnet*, *thin film magnet*, or *multilayer magnet*.
A magnet may have a *granular microstructure*. 

%BRANCHFIG Magnet addnodes=1 parents=0 rankdir='LR' relations=isA,hasSpatialPart,hasSpatialTile edgelabels=1 caption='A Magnet and its parts.'

%HEADER "Granular Microstructure" level=2  

The spatial parts of the granular microstructure are
the *main magnetic phase*, the *grain boundary phase*, and *secondary phase*.

The granular microstructure constists of a *main magnetic phase*, possible *grain boundary phases* and *secondary phases*.  

%BRANCHFIG GranularMicrostructure addnodes=1 parents=1 rankdir='LR' relations=isA,hasSpatialPart,hasSpatialTile edgelabels=1 caption='The granular microstructure of a magnet.'

%HEADER "Magnetic material" level=2  

The main magnetic phase is a *magnetic material*. A magnetic material has
*intrinsic magnetic properties* and a *chemical composition*. A magnetic material can be amorphous
or crystalline.

%BRANCHFIG MagneticMaterial addnodes=1 parents=0 rankdir='LR' relations=all edgelabels=1 caption='A magnetic material and its relations.'

%HEADER "Crystalline magnetic material" level=2  

A *crystalline magnetic material* is a *granular structure*. Properties of the granular structure are a *crystal structure* and a *grain size distribution*. *X-ray diffraction data* may have been measured.

%BRANCHFIG CrystallineMagneticMaterial addnodes=1 parents=1 rankdir='LR' relations=all edgelabels=1 caption='A crystalline magnetic material.'

%% you may add options to the documentation of a branch:  
%% (default values are listed below)  
%% caption=''      %% will give "Granular Microstructure branch.  
%% terminated=1    %% whether the graph should be terminated at leaf nodes  
%% strict_leaves=1 %% whether to strictly exclude leave descendants  
%% width=0px       %% optional figure width  
%% leaves=''       %% optional leaf node names for graph termination  
%% relations='all' %% comma-separated list of relations to include  
%% edgelabels=0    %% whether to include edgelabels  
%% rankdir='BT'    %% graph direction (BT, TB, RL, LR: bottom-top, top-bottom, right-left, left-right)  
%% legend=1        %% whether to add legend  
%% namespaces=''   %% sequence of names of namespaces to be included  
%% ontologies=''   %% sequence of names of ontologies to be included  
%% addnodes=1      %% whether to add missing target nodes in relations (1: True, 0: False)  
%% parents=1       %% Adds n levels of parents to graph  

%HEADER Classes level=2  
%ALL classes  

