#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ontopy import World
from owlready2 import Thing, DataProperty, ObjectProperty, locstr, AnnotationProperty
import sys
__version__ = "0.0.1"  # Version of this ontology

# From https://github.com/emmo-repo/domain-atomistic/blob/master/domain-atomistic.py
def en(s):
    """Returns `s` as an English location string."""
    return locstr(s, lang='en')

def pl(s):
    """Returns `s` as a plain literal string."""
    return locstr(s, lang='')

# Load EMMO
world = World(filename="demo.sqlite3")
emmo = world.get_ontology("data/emmo.ttl").load()  # https://emmo-repo.github.io/versions/1.0.0-rc3/emmo.ttl

# Examples can be found on:
# + https://github.com/emmo-repo/domain-atomistic/blob/master/domain-atomistic.py
# + https://github.com/emmo-repo/EMMOntoPy/blob/master/demo/vertical/define_ontology.py

# Create a new ontology with out extensions that imports EMMO
# TODO: Change the IRI to the correct one
# onto = world.get_ontology("http://w3id.org/emmo/domain/demo_magnetic_material#")
onto = world.get_ontology("http://www.emmc.info/emmc-csa/demo_magnetic_material#")
onto.imported_ontologies.append(emmo)

# Add new classes and object/data properties needed by the use case
with onto:

    # additional Annotation Properties
    
    class IECEntry(AnnotationProperty):
        pass
        
    class wikipediaReference(AnnotationProperty):
        pass

    class wikidataReference(AnnotationProperty):
        pass
        
    # crystal structure
    
    class Angstrom(emmo.DimensionalUnit):
        """Unit of length, equal to 10−10 metre, or 0.1 nanometre"""
        prefLabel = en("Angstrom")
        is_a = [emmo.hasSIConversionMultiplier.value("1.0E-10"),
                emmo.hasSIConversionOffset.value("0.0"),
                emmo.hasDimensionString.value("T0 L+1 M0 I0 Θ0 N0 J0")]        
        
    class SpaceGroup(emmo.NominalProperty):  # from define_ontology.py
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.
    
        It is identifies by its Hermann-Mauguin symbol or space group
        number (and setting) in the International tables of
        Crystallography."""
        prefLabel = en("SpaceGroup")
        is_a = [emmo.hasStringValue.exactly(1, emmo.String)]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q899033")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Space_group")
        
    class LatticeConstantA(emmo.Length):
        """The length of lattice vectors `a`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantA")
        altLabel = en("LatticeParameterA")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")
        is_a = [emmo.hasMeasurementUnit.some(Angstrom)]

    class LatticeConstantB(emmo.Length):
        """The length of lattice vectors `b`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantB")
        altLabel = en("LatticeParameterB")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")
        is_a = [emmo.hasMeasurementUnit.some(Angstrom)]

    class LatticeConstantC(emmo.Length):
        """The length of lattice vectors `c`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantC")
        altLabel = en("LatticeParameterC")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")
        is_a = [emmo.hasMeasurementUnit.some(Angstrom)]

    class LatticeConstantAlpha(emmo.Angle):
        """The angle between lattice vectors `b` and `c`, where lattice vectors `a`, `b` and `c` defines the unit cell,"""
        prefLabel = en("LatticeConstantAlpha")
        altLabel = en("LatticeParameterAlpha")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class LatticeConstantBeta(emmo.Angle):
        """The angle between lattice vectors `a` and `c`, where lattice vectors `a`, `b` and `c` defines the unit cell,"""
        prefLabel = en("LatticeConstantBeta")
        altLabel = en("LatticeParameterBeta")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class LatticeConstantGamma(emmo.Angle):
        """The angle between lattice vectors `a` and `b`, where lattice vectors `a`, `b` and `c` defines the unit cell,"""
        prefLabel = en("LatticeConstantGamma")
        altLabel = en("LatticeParameterGamma")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class CellVolume(emmo.Volume):
        """Volume of the unit cell."""
        prefLabel = en("CellVolume")
        altLabel = en("UnitCellVolume")
        
    class CrystalStructure(emmo.Crystal):
        """Description of ordered arrangement of atoms"""
        prefLabel = en("CrystalStructure")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q895901")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Crystal_structure")
        is_a = [
                emmo.hasProperty.exactly(1, SpaceGroup),
                emmo.hasProperty.exactly(1, LatticeConstantA),
                emmo.hasProperty.exactly(1, LatticeConstantB),
                emmo.hasProperty.exactly(1, LatticeConstantC),
                emmo.hasProperty.exactly(1, LatticeConstantAlpha),
                emmo.hasProperty.exactly(1, LatticeConstantBeta),
                emmo.hasProperty.exactly(1, LatticeConstantGamma),
                emmo.hasProperty.exactly(1, CellVolume),
                ]

        
    # energy density
    
    class EnergyDensityUnit(emmo.DimensionalUnit):  
        """Energy Density."""
        prefLabel = en("EnergyDensityUnit")
        is_a = [emmo.hasDimensionString.value("T-2 L-1 M+1 I0 Θ0 N0 J0"),  
        ]
    
    class EnergyDensity(emmo.PhysicalQuantity):
        """Energy Density."""
        prefLabel = en("EnergyDensity")
        is_a = [emmo.hasMeasurementUnit.some(EnergyDensityUnit),
               ]

    class LineEnergy(emmo.PhysicalQuantity):
        """Energy per unit length."""
        prefLabel = en("LineEnergy")
        is_a = [emmo.hasMeasurementUnit.some(emmo.JoulePerMetre),
        ]

    
    # intrinisc magnetic properties

    class SpontaneousMagnetization(emmo.Magnetization):
        """Spontaneous magnetization: The spontaneous magnetization of a ferromagnet is the result of alignment of the magnetic moments of  individual atoms. Ms exists within a domain of a ferromagnet.""" 
        prefLabel = en("SpontaneousMagnetization")
        altLabel = pl("Ms")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-41")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Spontaneous_magnetization")
        
    class SpontaneousMagneticPolarisation(emmo.MagneticPolarisation):
        """Spontaneous magnetic polarisation: The spontaneous magnetic polarisation of a ferromagnet is the result of alignment of the magnetic moments of  individual atoms. Js exists within a domain of a ferromagnet.""" 
        prefLabel = en("SpontaneousMagneticPolarisation")
        altLabel = pl("Js")
        
    class MagnetocrystallineAnisotropyEnergy(EnergyDensity):
        """The magnetocrystalline anisotropy energy density."""
        prefLabel = en("MagnetocrystallineAnisotropyEnergy")
        altLabel = en("MAE")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy")   
        
    class MagnetocrystallineAnisotropyConstantK1(EnergyDensity):
        """The magnetocrystalline constant K1 for tetragonal or hexagonal crystals."""
        comment = pl("Ea = K1 sin^2(phi) + K2 sin^4(phi) where Ea is the is the anisotropy energ density and phi is the angle of the magnetization with respect to the c-axis of the crystal.")
        prefLabel = en("MagnetocrystallineAnisotropyConstantK1")
        altLabel = en("K1")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy") 

    class MagnetocrystallineAnisotropyConstantK2(EnergyDensity):
        """The magnetocrystalline constant K2 for tetragonal or hexagonal crystals."""
        comment = pl("Ea = K1 sin^2(phi) + K2 sin^4(phi) where Ea is the is the anisotropy energ density and phi is the angle of the magnetization with respect to the c-axis of the crystal.")
        prefLabel = en("MagnetocrystallineAnisotropyConstantK2")
        altLabel = en("K2")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy") 

    class MagnetocrystallineAnisotropyConstantK1c(EnergyDensity):
        """The magnetocrystalline constant K1c for cubic crystals."""
        comment = pl("Ea = K1c(a1²a2²+a2²a3²+a1²a3²)+K1c(a1²a2²a3²) where Ea is the anisotropy energ density and a1,a2,a3 are the direction cosines of the magnetization")
        prefLabel = en("MagnetocrystallineAnisotropyConstantK1c")
        altLabel = en("K1")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy") 

    class MagnetocrystallineAnisotropyConstantK2c(EnergyDensity):
        """The magnetocrystalline constant K2c for cubic crystals"""
        comment = pl("Ea = K1c(a1²a2²+a2²a3²+a1²a3²)+K1c(a1²a2²a3²) where Ea is the anisotropy energ density and a1,a2,a3 are the direction cosines of the magnetization")
        prefLabel = en("MagnetocrystallineAnisotropyConstantK1c")
        altLabel = en("K1")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy") 

    class MagnetocrystallineAnisotropy(onto.Property):
        """Magnetocrystalline anisotropy is an intrinsic property. The magnetization process is different when the field is applied along different crystallographic directions, and the anisotropy reflects the crystal symmetry. Its origin is in the crystal-field interaction and spin-orbit coupling, or else the interatomic dipole–dipole interaction."""        
        prefLabel = en("MagnetocrystallineAnisotropy")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q6731660")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy")

    class ExchangeStiffnessConstant(LineEnergy):
        """Exchange constant in the continuum theory of micromagnetism"""
        prefLabel = en("MagnetocrystallineAnisotropy")
        altLable = en("A")

    class IntrinsicMagneticProperties(onto.Property):
        """Intrinsic magnetic material Properties."""
        prefLabel = en("IntrinsicMagneticProperties") 
        is_a = [
                emmo.hasProperty.exactly(1, SpontaneousMagnetization),
                emmo.hasProperty.some(SpontaneousMagneticPolarisation),
                emmo.hasProperty.some(MagnetocrystallineAnisotropy),
                emmo.hasProperty.some(ExchangeStiffnessConstant),
                emmo.hasProperty.exactly(1, emmo.CurieTemperature),
                ]

    # Magnetic material
    
    class MagneticMaterial(emmo.Material):
        """Magnetic material."""
        prefLabel = en("MagneticMaterial")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q11587827")
        is_a = [               
                emmo.hasSpatialDirectPart.some(emmo.PhaseOfMatter), 
                emmo.hasProperty.some(emmo.ChemicalComposition), 
                emmo.hasProperty.some(CrystalStructure),              
                emmo.hasProperty.exactly(1, IntrinsicMagneticProperties),
               ]

onto.sync_attributes(name_policy='uuid', class_docstring='elucidation',name_prefix='EMMO_')

#################################################################
# Annotate the ontology metadata
#################################################################
onto.metadata.comment.append("Created within the EU project MaMMoS. Grant number 101135546 (HORIZON-CL4-2023-DIGITAL-EMERGING-01)")

onto.metadata.abstract.append(en(
        'An EMMO-based ontology for magnetic materials.'
        'Created within the EU project MaMMoS. Grant number 101135546 (HORIZON-CL4-2023-DIGITAL-EMERGING-01)'
        'MagneticMaterial is released under the Creative Commons Attribution 4.0 '
        'International license (CC BY 4.0).'))

onto.metadata.title.append(en('Magnetic Material'))
onto.metadata.creator.append(en('Wilfried Hortschitz'))
onto.metadata.contributor.append(en('DISS-UWK'))
onto.metadata.versionInfo.append(en(__version__))
onto.metadata.comment.append(en(
    'Contacts:\n'
    'Wilfried Hortschitz\n'
    'DISS-UWK\n'
    'email: wilfried.hortschitz@donau-uni.ac.at\n'
    ))

# set version of ontology
onto.set_version(str(__version__))
onto.save("magnetic_material_mammos.ttl", overwrite=True)
