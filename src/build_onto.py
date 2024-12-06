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
        
    ### space group and lattice constants
    
    class SpaceGroup(emmo.NominalProperty):  # from define_ontology.py
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.
        
        The complete symmetry of a crystal, including the Bravais lattice and 
        any translational symmetry elements, is given by one of the 240 space groups.
    
        A space group is identified by its Hermann-Mauguin symbol or space group
        number (and setting) in the International tables of
        Crystallography."""
        prefLabel = en("SpaceGroup")
        is_a = [emmo.hasStringValue.some(emmo.String)]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q899033")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Space_group")
        
    class LatticeConstantA(emmo.Length):
        """The length of lattice vectors `a`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantA")
        altLabel = en("LatticeParameterA")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

    class LatticeConstantB(emmo.Length):
        """The length of lattice vectors `b`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantB")
        altLabel = en("LatticeParameterB")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

    class LatticeConstantC(emmo.Length):
        """The length of lattice vectors `c`, where lattice vectors `a`, `b` and `c` defines the unit cell"""
        prefLabel = en("LatticeConstantC")
        altLabel = en("LatticeParameterC")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

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

    #-----------------------------------------------------
        
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

    #-----------------------------------------------------
        
    ### energy densities

    class EnergyDensity(emmo.PhysicalQuantity):
        """Energy Density."""
        prefLabel = en("EnergyDensity")
        is_a = [emmo.hasMeasurementUnit.some(emmo.JoulePerCubicMetre),
               ]

    class LineEnergy(emmo.PhysicalQuantity):
        """Energy per unit length."""
        prefLabel = en("LineEnergy")
        is_a = [emmo.hasMeasurementUnit.some(emmo.JoulePerMetre),
               ]

    
    # intrinisc magnetic properties

    ## magnetization
    
    class SpontaneousMagnetization(emmo.ElectromagneticQuantity):
        """The spontaneous magnetization, Ms, of a ferromagnet is the result of alignment of the magnetic moments of  individual atoms. Ms exists within a domain of a ferromagnet.""" 
        prefLabel = en("SpontaneousMagnetization")
        altLabel = pl("Ms")
        IECEntry = pl("https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-41")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Spontaneous_magnetization")
        
    class SpontaneousMagneticPolarisation(emmo.ElectromagneticQuantity):
        """She spontaneous magnetic polarisation, Js, of a ferromagnet is the result of alignment of the magnetic moments of  individual atoms. Js exists within a domain of a ferromagnet.""" 
        prefLabel = en("SpontaneousMagneticPolarisation")
        altLabel = pl("Js")
        
    ## magnetocrystalline anisotropy
    
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

    ## Exchange
    
    class ExchangeStiffnessConstant(LineEnergy):
        """Exchange constant, A, in the continuum theory of micromagnetism.
        
        The exchange stiffness A is related to the Curie temperature TC: A is roughly
        k_B T_c/(2 a_0), where a_0 is the lattice parameter in a simple structure."""
        prefLabel = en("ExchangeStiffnessConstant")
        altLable = en("A")
        
    #-----------------------------------------------------

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

    #-----------------------------------------------------

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
               
    # Other relevant Quantities

    #class ExternalField(emmo.    
               
    # Extrinsic magnetic properties
    
    class CoercivityHc(emmo.Coercivity):
        """The internal magnetic held -Hc at which the macroscopic magnetization vanishes is the coercivity or coercive force.
        
        Although it is not an intrinsic property in our sense of the term, the M-H loop coercivity Hc is
        sometimes referred to as 'intrinsic' coercivity.
        """
        prefLabel = en("CoercivityHc")
        altLabel = en("Coercive field, Hc")
    
    class CoercivityBHc(emmo.Coercivity):
        """Defined as internal field on the B(H) loop where B = 0. It is also called flux coerciviy BHc.
        
        BHc depends on sample shape and has to be corrected for the demagnetizing field."""
        prefLabel = en("CoercivityBHc")
        altLabel = en("BHc")   

    class CoercivityHcPrime(emmo.Coercivity):
        """The external magnetic held -H'c at which the macroscopic magnetization vanishes. 
        The coercivity on M(H') loop, where H' is the external field."""
        prefLabel = en("CoercivityHcPrime")
        altLabel = en("Coercive field, H'c")
    
    class CoercivityBHcPrime(emmo.Coercivity):
        """Defined as external field on the B(H') loop where B = 0. H' is the external field."""
        prefLabel = en("CoercivityBHcPrime")
        altLabel = en("BH'c")   

    class SwtichingFieldCoercivity(emmo.MagneticFieldStrength):
        """Defined by the maximum slope of the descending branch of the M-H hysteresis loop, with H the internal field."""
        comment = pl("This field is often used when analysing the temperature dependend coercivity for deriving the microstructural parameters")
        prefLabel = en("SwitchingFieldCoercivity")
        altLabel = en("Hsw")   

    class SwtichingFieldCoercivityPrime(emmo.MagneticFieldStrength):
        """Defined by the maximum slope of the descending branch of the M-H' hysteresis loop, with H' the external field."""
        prefLabel = en("SwitchingFieldCoercivityPrime")
        altLabel = en("H'sw")   

    class KneeField(emmo.MagneticFieldStrength):
        """The maximum working field - also named knee field H_K, is defined as the reverse internal field for which the
        magnetization is reduced by 10%; thus it corresponds to the point on the
        magnetization loop for which M = 0.9 Mr (J = 0.9 Jr)"""
        altLabel = en("maximum working field, Hk")

    class KneeFieldPrime(emmo.MagneticFieldStrength):
        """The maximum working field - also named knee field H_K, is defined as the reverse external field for which the
        magnetization is reduced by 10%; thus it corresponds to the point on the magnetization loop for which M = 0.9 Mr (J = 0.9 Jr)"""
        altLabel = en("H'k")


    #-----------------------------------------------------

    class ExtrinsicMagneticMaterialProperty(onto.Property):
        """Extrinsic magnetic material Properties depend on the microstructure of the specimen."""
        prefLabel = en("ExtrinsicMagneticMaterialProperty")
        # 
        is_a = [emmo.hasProperty.exactly(1, emmo.Coercivity),
                #emmo.hasProperty.exactly(1, Remanence),
                #emmo.hasProperty.exactly(1, MagneticKneeField),
                #emmo.hasProperty.exactly(1, SaturationMagnetization),
                #emmo.hasProperty.exactly(1, MagnetizationTemperature),
                #emmo.hasProperty.exactly(1, DemagnetizationFactor),    
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
