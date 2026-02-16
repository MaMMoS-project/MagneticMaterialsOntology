#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ontopy import World
from owlready2 import (
    locstr,
    AnnotationProperty,
    Not,
)

__version__ = "0.0.4"  # Version of this ontology


# From https://github.com/emmo-repo/domain-atomistic/blob/master/domain-atomistic.py
def en(s):
    """Returns `s` as an English location string."""
    return locstr(s, lang="en")


def enGB(s):
    """Returns `s` as an British-English location string."""
    return locstr(s, lang="en-GB")


def enUS(s):
    """Returns `s` as an American-English location string."""
    return locstr(s, lang="en-US")


def pl(s):
    """Returns `s` as a plain literal string."""
    return locstr(s, lang="")


# Append a new altLabel to an EMMO entry: if the entry already
# has an altLabel list, append the value; otherwise create altLabel
# as a new list containing the value.
def add_altLabel(entry, label):
    if hasattr(entry, "altLabel"):
        entry.altLabel.append(label)
    else:
        entry.altLabel = [label]


# Load specific version of EMMO
world = World(filename="magnetic-materials.sqlite3")
emmo = world.get_ontology(
    "https://emmo-repo.github.io/versions/1.0.3/emmo-inferred.ttl"
).load()

# Create a new ontology with out extensions that imports EMMO
onto = world.get_ontology("https://w3id.org/emmo/domain/magnetic-materials#")
onto.imported_ontologies.append(emmo)

# Add new classes and object/data properties needed by the use case
with onto:
    # Additional Annotation Properties

    class IECEntry(AnnotationProperty):
        pass

    class wikipediaReference(AnnotationProperty):
        pass

    class wikidataReference(AnnotationProperty):
        pass

    # Crystal structure

    # # Space group and lattice constants

    class SpaceGroup(emmo.NominalProperty):  # from define_ontology.py
        """A spacegroup is the symmetry group of all symmetry operations
        that apply to a crystal structure.

        The complete symmetry of a crystal, including the Bravais lattice and
        any translational symmetry elements, is given by one of the 240 space
        groups.

        A space group is identified by its Hermann-Mauguin symbol or space
        group number (and setting) in the International tables of
        Crystallography."""

        prefLabel = en("SpaceGroup")
        is_a = [emmo.hasStringValue.some(emmo.String)]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q899033")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Space_group")

    class LatticeConstantA(emmo.Length):
        """The length of lattice vectors `a`, where lattice vectors
        `a`, `b` and `c` define the unit cell."""

        prefLabel = en("LatticeConstantA")
        altLabel = en("LatticeParameterA")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13"
        )
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

    class LatticeConstantB(emmo.Length):
        """The length of lattice vectors `b`, where lattice vectors `a`, `b`
        and `c` define the unit cell."""

        prefLabel = en("LatticeConstantB")
        altLabel = en("LatticeParameterB")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13"
        )
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

    class LatticeConstantC(emmo.Length):
        """The length of lattice vectors `c`, where lattice vectors `a`, `b`
        and `c` define the unit cell."""

        prefLabel = en("LatticeConstantC")
        altLabel = en("LatticeParameterC")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=561-07-13"
        )
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Lattice_constant")

    class LatticeConstantAlpha(emmo.Angle):
        """The angle between lattice vectors `b` and `c`, where lattice
        vectors `a`, `b` and `c` define the unit cell."""

        prefLabel = en("LatticeConstantAlpha")
        altLabel = en("LatticeParameterAlpha")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class LatticeConstantBeta(emmo.Angle):
        """The angle between lattice vectors `a` and `c`, where lattice
        vectors `a`, `b` and `c` define the unit cell."""

        prefLabel = en("LatticeConstantBeta")
        altLabel = en("LatticeParameterBeta")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class LatticeConstantGamma(emmo.Angle):
        """The angle between lattice vectors `a` and `b`, where lattice
        vectors `a`, `b` and `c` define the unit cell."""

        prefLabel = en("LatticeConstantGamma")
        altLabel = en("LatticeParameterGamma")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q625641")

    class CellVolume(emmo.Volume):
        """Volume of the unit cell."""

        prefLabel = en("CellVolume")
        altLabel = en("UnitCellVolume")

    # -----------------------------------------------------
    class CrystalStructure(emmo.Property):
        """Description of ordered arrangement of atoms."""

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

    # -----------------------------------------------------

    # energy densities

    class EnergyDensityUnit(emmo.SIDimensionalUnit):
        """Unit of energy density. Defined using SI base units."""

        prefLabel = en("EnergyDensityUnit")
        is_a = [emmo.hasDimensionString.value("T-2 L-1 M+1 I0 Θ0 N0 J0")]

    # Assert JoulePerCubicMetre as subclass of EnergyDensityUnit
    emmo.JoulePerCubicMetre.is_a.append(EnergyDensityUnit)
    add_altLabel(emmo.JoulePerCubicMetre, enUS("JoulePerCubicMeter"))
    add_altLabel(emmo.JoulePerCubicMetre, enGB("JoulePerCubicMetre"))
    # Assert MegaJoulePerCubicMetre as subclass of EnergyDensityUnit
    emmo.MegaJoulePerCubicMetre.is_a.append(EnergyDensityUnit)
    add_altLabel(emmo.MegaJoulePerCubicMetre, enGB("MegaJoulePerCubicMetre"))
    add_altLabel(emmo.MegaJoulePerCubicMetre, enUS("MegaJoulePerCubicMeter"))

    class EnergyDensity(emmo.PhysicalQuantity):
        """Energy Density."""

        prefLabel = en("EnergyDensity")
        is_a = [
            emmo.hasMeasurementUnit.some(EnergyDensityUnit),
        ]

    class LineEnergyUnit(emmo.SIDimensionalUnit):
        """Unit of energy per unit length. Defined using SI base units."""

        prefLabel = en("LineEnergyUnit")
        is_a = [emmo.hasDimensionString.value("T-2 L+1 M+1 I0 Θ0 N0 J0")]

    # Assert JoulePerMetre as subclass of LineEnergyUnit
    emmo.JoulePerMetre.is_a.append(LineEnergyUnit)
    add_altLabel(emmo.JoulePerMetre, enUS("JoulePerMeter"))
    add_altLabel(emmo.JoulePerMetre, enGB("JoulePerMetre"))

    class LineEnergy(emmo.PhysicalQuantity):
        """Energy per unit length."""

        prefLabel = en("LineEnergy")
        altLabel = [en("EnergyPerUnitLength"), en("EnergyPerLength")]
        is_a = [
            emmo.hasMeasurementUnit.some(LineEnergyUnit),
        ]

    # intrinsic magnetic properties

    ## magnetization

    add_altLabel(emmo.Magnetization, enUS("VolumeMagnetization"))
    add_altLabel(emmo.Magnetization, enGB("VolumeMagnetisation"))
    add_altLabel(emmo.Magnetization, enUS("Magnetization"))
    add_altLabel(emmo.Magnetization, enGB("Magnetisation"))

    class MassMagnetizationUnit(emmo.SIDimensionalUnit):
        """Class of units of the magnetization per unit mass.
        Defined using SI base units."""

        prefLabel = en("MassMagnetizationUnit")
        altLabel = [
            enUS("MassMagnetizationUnit"),
            enGB("MassMagnetisationUnit"),
            enUS("SpecificMagnetizationUnit"),
            enGB("SpecificMagnetisationUnit"),
        ]
        is_a = [emmo.hasDimensionString.value("T0 L+2 M-1 I+1 Θ0 N0 J0")]

    class AmpereSquareMetrePerKilogram(MassMagnetizationUnit):
        """Unit of the magnetic moment per unit mass: Am²/kg."""

        prefLabel = en("AmpereSquareMetrePerKilogram")
        altLabel = [
            enUS("AmpereSquareMeterPerKilogram"),
            enGB("AmpereSquareMetrePerKilogram"),
        ]
        unitSymbol = en("A⋅m²/kg")
        ucumCode = en("A.m2.kg-1")

    class MagneticMomentPerUnitMass(emmo.ElectromagneticQuantity):
        """Magnetic moment per unit mass, sigma."""

        comment = en(
            "The magnetization is obtained by multiplying sigma with \
                     the density"
        )
        prefLabel = en("MagneticMomentPerUnitMass")
        altLabel = [
            en("SpecificMagneticMoment"),
            enUS("MassMagnetization"),
            enGB("MassMagnetisation"),
            pl("sigma"),
        ]

        is_a = [emmo.hasMeasurementUnit.some(MassMagnetizationUnit)]

    class SpontaneousMagnetization(emmo.ElectromagneticQuantity):
        """The spontaneous magnetization, Ms, of a ferromagnet is the result
        of alignment of the magnetic moments of individual atoms. Ms exists
        within a domain of a ferromagnet."""

        prefLabel = en("SpontaneousMagnetization")
        altLabel = [
            enUS("SpontaneousMagnetization"),
            enGB("SpontaneousMagnetisation"),
            pl("Ms"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-41"
        )
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Spontaneous_magnetization"
        )

    class SpontaneousMagneticPolarisation(emmo.ElectromagneticQuantity):
        """The spontaneous magnetic polarisation, Js, of a ferromagnet is the
        result of alignment of the magnetic moments of  individual atoms.
        Js exists within a domain of a ferromagnet."""

        prefLabel = en("SpontaneousMagneticPolarization")
        altLabel = [
            enUS("SpontaneousMagneticPolarization"),
            enGB("SpontaneousMagneticPolarisation"),
            pl("Js"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFluxDensityUnit)]

    ## anisotropy

    class MagneticAnisotropy(emmo.Property):
        """Magnetic anisotropy means that the magnetic properties depend on
        the direction in which they are measured."""

        prefLabel = en("MagneticAnisotropy")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetic_anisotropy")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-01-08"
        )

    class RectangularCuboid(emmo.EuclideanSpace):
        """A rectangular cuboid is a special case of a cuboid with rectangular
        faces in which all of its dihedral angles are right angles."""

        prefLabel = en("RectangularCuboid")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q262959")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Rectangular_cuboid")

    class GeometricalSize(emmo.Property):
        """Spatial extension along the principal axes."""

        prefLabel = en("GeometricalSize")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Size")
        is_a = [emmo.hasProperty.exactly(3, emmo.Length)]

    class GeometricShape(emmo.Property, emmo.Geometrical):
        """Geometric shape.

        Two extrinsic properties, the remanence Mr
        and coercivity Hc, which depend on the sample shape
        """

        prefLabel = en("GeometricShape")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q207961")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Shape")
        is_a = [emmo.hasSpatialDirectPart.exactly(1, emmo.Cylinder | RectangularCuboid)]

    class SampleGeometry(emmo.Property):
        """The size and shape of the magnet"""

        prefLabel = en("SampleGeometry")
        is_a = [
            emmo.hasProperty.exactly(1, GeometricalSize),
            emmo.hasProperty.exactly(1, GeometricShape),
        ]

    class DemagnetizingFactor(emmo.ElectromagneticQuantity):
        """For a uniformly magnetized ellipsoid with magnetization along a
        major axis the demagnetizing field is Hd = -N M.

        The principal components of the diagonal demagnetizing tensor form
        the demagnetizing factors. Only two of the three are independent
        because the demagnetizing tensor has unit trace Nx + Ny + Nz = 1.
        """

        comment = pl(
            "H = H' - DM, where D is the demagnetizing factor, M is the \
            magnetization, and H is the internal field."
        )
        prefLabel = en("DemagnetizingFactor")
        altLabel = [
            enUS("DemagnetizingFactor"),
            enGB("DemagnetisingFactor"),
            pl("N"),
            pl("D"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=121-12-63"
        )

    class ShapeAnisotropyConstant(EnergyDensity):
        """The energy density of a small particle given by

        K1sh = (mu_0/4)(1-3D)Ms²

        where mu_0 is the vacuum magnetic permeability and D is the
        DemagnetizingFactor and Ms is the spontaneous magnetization.
        """

        prefLabel = en("ShapeAnisotropyConstant")
        altLabel = pl("K1sh")

    class ShapeAnisotropy(MagneticAnisotropy):
        """The difference in magnetostatic energy when an elongated particle
        is magnetized along its short and long axis.
        """

        comment = en(
            "Shape anisotropy is restricted to small particles, where \
            the inter-atomic exchange ensures a uniform  magnetization."
        )
        prefLabel = en("ShapeAnisotropy")
        is_a = [
            emmo.hasProperty.exactly(1, DemagnetizingFactor),
            emmo.hasProperty.exactly(1, ShapeAnisotropyConstant),
        ]

    ## magnetocrystalline anisotropy

    class MagnetocrystallineAnisotropyEnergy(EnergyDensity):
        """The magnetocrystalline anisotropy energy density."""

        prefLabel = en("MagnetocrystallineAnisotropyEnergy")
        altLabel = pl("MAE")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )

    class AnisotropyField(emmo.MagneticFieldStrength):
        """The anisotropy field Ha is defined as the field needed to
        saturate the magnetization of a uniaxial crystal in a hard direction.
        Ha = 2 Ku/Js
        """

        comment = en(
            "Beware of taking the idea of anisotropy field too literally. \
            Except at small angles, the energy variation in a field is \
            not the same as the leading term in the anisotropy. \
            A magnetic field defines an easy direction, not an easy axis."
        )
        prefLabel = en("AnisotropyField")
        altLabel = pl("Ha")

    class UniaxialAnisotropyConstant(EnergyDensity):
        """The change of energy with angle of the magnetization from
        the preferred direction is expressed with the
        uniaxial anisotropy constant Ea = Ku sin²(theta)."""

        prefLabel = en("UniaxialAnisotropyConstant")
        altLabel = pl("Ku")

    class UniaxialMagneticAnisotropy(MagneticAnisotropy):
        """The anisotropy can be described as uniaxial when the anisotropy
        energy E depends on only a single angle, the angle between the
        magnetization vector and the easy direction of magnetization.
        """

        prefLabel = en("UniaxialMagneticAnisotropy")
        is_a = [
            emmo.hasProperty.exactly(1, AnisotropyField),
            emmo.hasProperty.exactly(1, UniaxialAnisotropyConstant),
        ]

    class InducedMagneticAnisotropy(UniaxialMagneticAnisotropy):
        """Uniaxial anisotropy induced by annealing in a magnetic field or
        by applying a stress."""

        prefLabel = en("InducedMagneticAnisotropy")

    class MagnetocrystallineAnisotropyConstantK1(EnergyDensity):
        """The magnetocrystalline constant K1 for tetragonal or
        hexagonal crystals."""

        comment = pl(
            "Ea = K1 sin^2(phi) + K2 sin^4(phi) where Ea is the is the \
            anisotropy energy density and phi is the angle of the \
            magnetization with respect to the c-axis of the crystal."
        )
        prefLabel = en("MagnetocrystallineAnisotropyConstantK1")
        altLabel = pl("K1")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )

    class MagnetocrystallineAnisotropyConstantK2(EnergyDensity):
        """The magnetocrystalline constant K2 for tetragonal or
        hexagonal crystals."""

        comment = pl(
            "Ea = K1 sin^2(phi) + K2 sin^4(phi) where Ea is the is the \
            anisotropy energy density and phi is the angle of the \
            magnetization with respect to the c-axis of the crystal."
        )
        prefLabel = en("MagnetocrystallineAnisotropyConstantK2")
        altLabel = pl("K2")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )

    class MagnetocrystallineAnisotropyConstantK1c(EnergyDensity):
        """The magnetocrystalline constant K1c for cubic crystals."""

        comment = pl(
            "Ea = K1c(a1²a2²+a2²a3²+a1²a3²)+K2c(a1²a2²a3²) where Ea is \
            the anisotropy energy density and a1,a2,a3 are the direction \
            cosines of the magnetization"
        )
        prefLabel = en("MagnetocrystallineAnisotropyConstantK1c")
        altLabel = pl("K1c")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )

    class MagnetocrystallineAnisotropyConstantK2c(EnergyDensity):
        """The magnetocrystalline constant K2c for cubic crystals."""

        comment = pl(
            "Ea = K1c(a1²a2²+a2²a3²+a1²a3²)+K2c(a1²a2²a3²) where Ea is the \
            anisotropy energy density and a1,a2,a3 are the direction \
            cosines of the magnetization"
        )
        prefLabel = en("MagnetocrystallineAnisotropyConstantK2c")
        altLabel = pl("K2c")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )

    class UniaxialMagnetocrystallineAnisotropy(UniaxialMagneticAnisotropy):
        """The uniaxial anisotropy depends on only a single angle, the angle
        magnetization vector and the c axis.
        """

        prefLabel = en("UniaxialMagnetocrystallineAnisotropy")
        is_a = [
            emmo.hasProperty.exactly(1, MagnetocrystallineAnisotropyConstantK1),
            emmo.hasProperty.min(0, MagnetocrystallineAnisotropyConstantK2),
        ]

    class CubicMagnetocrystallineAnisotropy(MagneticAnisotropy):
        """Cubic crystals anisotropy."""

        prefLabel = en("CubicMagnetocrystallineAnisotropy")
        is_a = [
            emmo.hasProperty.exactly(1, MagnetocrystallineAnisotropyConstantK1c),
            emmo.hasProperty.min(0, MagnetocrystallineAnisotropyConstantK2c),
        ]

    class MagnetocrystallineAnisotropy(emmo.Property):
        """Magnetocrystalline anisotropy is an intrinsic property. The
        magnetisation process is different when the field is applied along
        different crystallographic directions, and the anisotropy reflects
        the crystal symmetry. Its origin is in the crystal-field interaction
        and spin-orbit coupling, or else the interatomic dipole–dipole
        interaction."""

        prefLabel = en("MagnetocrystallineAnisotropy")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q6731660")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magnetocrystalline_anisotropy"
        )
        is_a = [
            emmo.hasProperty.exactly(
                1,
                UniaxialMagnetocrystallineAnisotropy
                | CubicMagnetocrystallineAnisotropy,
            )
        ]

    ## Exchange

    class ExchangeStiffnessConstant(LineEnergy):
        """Exchange constant, A, in the continuum theory of micromagnetism.

        The exchange stiffness A is related to the Curie temperature TC:
        A is roughly k_B T_c/(2 a_0), where a_0 is the lattice parameter in
        a simple structure."""

        prefLabel = en("ExchangeStiffnessConstant")
        altLabel = pl("A")

    # ----------------------------------------------------
    class IntrinsicMagneticProperties(emmo.Property):
        """Intrinsic magnetic properties refer to atomic-scale magnetism and
        depend on the crystal structure."""

        prefLabel = en("IntrinsicMagneticProperties")
        is_a = [
            emmo.hasProperty.some(SpontaneousMagnetization),
            emmo.hasProperty.some(SpontaneousMagneticPolarisation),
            emmo.hasProperty.some(MagnetocrystallineAnisotropy),
            emmo.hasProperty.some(ExchangeStiffnessConstant),
            emmo.hasProperty.some(emmo.CurieTemperature | emmo.NeelTemperature),
        ]

    # -----------------------------------------------------

    # Characterisation data

    ### XRD

    class XrdTwoThetaAngles(emmo.Vector):
        """The 2theta angles at which the counts are measured during X-ray
        diffraction."""

        prefLabel = en("XrdTwoThetaAngles")
        altLabel = en("XRDTwoThetaAngles")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.Degree),
        ]

    class XrdCounts(emmo.Vector):
        """Counts as a function of 2theta angle obtained from X-ray
        diffraction."""

        prefLabel = en("XrdCounts")
        altLabel = en("XRDCounts")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.CountingUnit),
        ]

    class XrayDiffractionData(emmo.Property, emmo.Matrix):
        """Counts as a function of 2theta angle obtained from X-ray
        diffraction."""

        prefLabel = en("XrayDiffractionData")
        is_a = [
            emmo.hasProperty.exactly(1, XrdTwoThetaAngles),
            emmo.hasProperty.exactly(1, XrdCounts),
        ]

    class Xrd2dImage(emmo.Property, emmo.Matrix):
        """2D array containing all pixel intensities from a 2D XRD camera.
        This is the raw XRD data from which 1D spectra are obtained."""

        prefLabel = en("Xrd2dImage")
        altLabel = [
            en("Xrd2DImage"),
            en("XRD2dImage"),
            en("XRD2DImage"),
        ]
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.CountingUnit),
        ]

    ### EDX (Energy-Dispersive X-ray Spectroscopy)

    class EdxEnergy(emmo.Vector):
        """The energy values at which the counts are measured during
        Energy-Dispersive X-ray spectroscopy."""

        prefLabel = en("EdxEnergy")
        altLabel = en("EDXEnergy")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.ElectronVolt),
        ]

    class EdxCounts(emmo.Vector):
        """Counts as a function of energy obtained from Energy-Dispersive
        X-ray spectroscopy."""

        prefLabel = en("EdxCounts")
        altLabel = en("EDXCounts")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.CountingUnit),
        ]

    class EdxData(emmo.Property, emmo.Matrix):
        """Counts as a function of energy obtained from Energy-Dispersive
        X-ray spectroscopy."""

        prefLabel = en("EdxData")
        altLabel = [
            en("EDXData"),
            en("EnergyDispersiveXraySpectroscopyData")
        ]
        is_a = [
            emmo.hasProperty.exactly(1, EdxEnergy),
            emmo.hasProperty.exactly(1, EdxCounts),
        ]

    ### MOKE (Magneto-Optic Kerr Effect)

    class MokeAppliedField(emmo.Vector):
        """The applied magnetic field values during MOKE measurement."""

        prefLabel = en("MokeAppliedField")
        altLabel = en("MOKEAppliedField")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit),
        ]

    class MokeKerrSignal(emmo.Vector):
        """The Kerr signal (rotation or ellipticity) as a function of
        applied field obtained from MOKE measurement."""

        prefLabel = en("MokeKerrSignal")
        altLabel = [
            en("MOKEKerrSignal"),
            en("KerrSignal"),
        ]
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit),
        ]

    class MokeData(emmo.Property, emmo.Matrix):
        """Kerr signal as a function of applied magnetic field obtained
        from Magneto-Optic Kerr Effect measurement."""

        prefLabel = en("MokeData")
        altLabel = [
            en("MOKEData"),
            en("MagnetoOpticKerrEffectData"),
        ]
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Magneto-optic_Kerr_effect"
        )
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=121-12-97"
        )
        is_a = [
            emmo.hasProperty.exactly(1, MokeAppliedField),
            emmo.hasProperty.exactly(1, MokeKerrSignal),
        ]

    ### Profilometry

    class ProfilDistance(emmo.Vector):
        """The distance values along the scan direction during
        profilometry measurement."""

        prefLabel = en("ProfilDistance")
        altLabel = en("PROFILDistance")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.LengthUnit),
        ]

    class ProfilTotalProfile(emmo.Vector):
        """The height profile as a function of distance obtained from
        profilometry measurement."""

        prefLabel = en("ProfilTotalProfile")
        altLabel = en("PROFILTotalProfile")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.LengthUnit),
        ]

    class ProfilometryData(emmo.Property, emmo.Matrix):
        """Height profile as a function of distance obtained from
        profilometry measurement."""

        prefLabel = en("ProfilometryData")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Profilometer")
        is_a = [
            emmo.hasProperty.exactly(1, ProfilDistance),
            emmo.hasProperty.exactly(1, ProfilTotalProfile),
        ]

    ### magnetic materials

    ### Grains and granular structure

    class EulerAngles(emmo.Quantity):
        """Three angles introduced by Leonhard Euler to describe the
        orientation of a rigid body with respect to a fixed coordinate
        system."""

        prefLabel = en("EulerAngles")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q751290")
        is_a = [emmo.hasProperty.exactly(3, emmo.Angle)]

    class CrystallographicOrientation(emmo.Property):
        """Relative direction of a crystallite in space with respect to
        another, disregarding distance."""

        prefLabel = en("CrystallographicOrientation")
        altLabel = pl("CrystalOrientation")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q11799166")
        is_a = [emmo.hasProperty.exactly(1, EulerAngles)]

    class GrainMisalignmentAngle(emmo.Angle):
        """Standard deviation of the angle of the easy axis with respect to
        the alignment direction.
        """

        prefLabel = en("GrainMisalignmentAngle")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q117089304")

    class EasyAxisDistributionSigma(emmo.Angle):
        """Standard deviation of the grain misalignment angle in an ensembles
        of misaligned magnetic particles.

        This refers not only to isotropic magnets but also to
        partly aligned or textured magnets, where the easy-axis distribution
        is described by a function P(theta).
        """

        prefLabel = en("EasyAxisDistributionSigma")

    class Grain(emmo.Crystal):
        """A grain is a small or even microscopic crystal which forms, for
        example, during the cooling of many materials."""

        prefLabel = en("Grain")
        altLabel = en("Crystallite")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q899604")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Crystallite")
        is_a = [
            emmo.hasProperty.exactly(1, CrystalStructure),
            emmo.hasProperty.exactly(1, emmo.ChemicalComposition),
            emmo.hasProperty.exactly(1, emmo.Diameter),
            emmo.hasProperty.exactly(
                1, CrystallographicOrientation | GrainMisalignmentAngle
            ),
        ]

    class MeanGrainSize(emmo.Length):
        """The mean of the grain diameter of grains. Diameter is the diameter
        of a sphere with equivalent volume."""

        prefLabel = en("MeanGrainSize")

    class SigmaGrainSize(emmo.Length):
        """The standard deviation of the grain diameter of grains. Diameter is
        the diameter of a sphere with equivalent volume."""

        prefLabel = en("SigmaGrainSize")

    class GrainSizeDistribution(emmo.Property):
        """Function representing relative sizes of grains in a system.
        Given by its mean and standard deviation of a lognormal distribution
        """

        prefLabel = en("GrainSizeDistribution")
        altLabel = en("ParticleSizeDistribution")
        wikipediaReference = pl(
            "https://en.wikipedia.org/wiki/Particle-size_distribution"
        )
        wikidataReference = pl("https://www.wikidata.org/wiki/Q2054937")
        is_a = [
            emmo.hasProperty.exactly(1, MeanGrainSize),
            emmo.hasProperty.exactly(1, SigmaGrainSize),
        ]

    class MagneticMaterial(emmo.MaterialByStructure):
        """Magnetically ordered solids which have atomic magnetic moments due
        to unpaired electrons."""

        prefLabel = en("MagneticMaterial")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q11587827")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.ChemicalComposition),
            emmo.hasProperty.exactly(1, emmo.Density),
            emmo.hasProperty.exactly(1, IntrinsicMagneticProperties),
        ]

    class AmorphousMagneticMaterial(emmo.AmorphousMaterial, MagneticMaterial):
        """Any amorphous structure entails a distribution of nearest-neighbour
        environments and bond lengths for a given magnetic atom, described by
        the radial distribution function and higher-order correlation
        functions. These distributions lead to a distribution of site moments,
        exchange interactions, dipolar and crystal fields, all of which
        influence the nature of the magnetic order."""

        prefLabel = en("AmorphousMagneticMaterial")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Amorphous_magnet")

    class GranularStructure(emmo.CrystallineMaterial):
        """Ensemble of grains of 1 or more grains."""

        prefLabel = en("GranularStructure")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.CrystalStructure),
            emmo.hasProperty.exactly(1, GrainSizeDistribution),
            emmo.hasProperty.min(0, XrayDiffractionData),
            emmo.hasSpatialPart.min(0, Grain),
        ]

    class NonMagneticMaterial(emmo.Material):
        """A material which is non-magnetic."""

        prefLabel = en("NonMagneticMaterial")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.ChemicalComposition),
            emmo.hasProperty.exactly(1, emmo.Density),
            emmo.hasSpatialPart.min(0, GranularStructure),
        ]

    class CrystallineMagneticMaterial(GranularStructure, MagneticMaterial):
        """Magnetic material with crystalline structure."""

        prefLabel = en("CrystallineMagneticMaterial")

    # Internal and external magnetic fields

    class ExternalMagneticField(emmo.ElectromagneticQuantity):
        """The external field H′, acting on a sample that is produced by
        electric currents or the stray field of magnets outside the sample
        volume, is often called the applied field."""

        prefLabel = en("ExternalMagneticField")
        altLabel = [
            en("AppliedMagneticField"),
            pl("H'"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]

    class DemagnetizingField(emmo.ElectromagneticQuantity):
        """The magnetic field produced by the magnetization distribution
        of the sample itself."""

        prefLabel = en("DemagnetizingField")
        altLabel = [
            enUS("DemagnetizingField"),
            enGB("DemagnetisingField"),
            pl("Hd"),
        ]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q5255001")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Demagnetizing_field")
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]

    class InternalMagneticField(emmo.ElectromagneticQuantity):
        """The internal field in the sample in the continuous medium
        approximation is the sum of the external field H′ and the
        demagnetizing field Hd."""

        prefLabel = en("InternalMagneticField")
        altLabel = pl("H")
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]

    # Hysteresis properties

    class CoercivityHc(emmo.Coercivity):
        """The internal magnetic field -Hc at which the macroscopic
        magnetization vanishes is the coercivity or coercive force.

        Although it is not an intrinsic property in our sense of the term,
        the M-H loop coercivity Hc is sometimes referred to as
        'intrinsic' coercivity.
        """

        prefLabel = en("CoercivityHc")
        altLabel = [
            en("CoercivityInternal"),
            en("CoercivityHcInternal"),
            en("CoerciveField"),
            pl("Hc"),
        ]
        IECEntry = [
            pl(
                "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-35"
            ),
            pl(
                "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=121-12-69"
            ),
            pl(
                "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-36"
            ),
        ]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q432635")

    class CoercivityBHc(emmo.Coercivity):
        """Defined as internal field on the B(H) loop where B = 0.
        It is also called flux coercivity BHc.

        BHc depends on sample shape and has to be corrected for the
        demagnetizing field.
        """

        prefLabel = en("CoercivityBHc")
        altLabel = pl("BHc")

    class CoercivityHcExternal(emmo.Coercivity):
        """The external magnetic field -H'c at which the macroscopic
        magnetization vanishes.
        The coercivity on M(H') loop, where H' is the external field."""

        prefLabel = en("CoercivityHcExternal")
        altLabel = pl("H'c")

    class CoercivityBHcExternal(emmo.Coercivity):
        """Defined as external field on the B(H') loop where
        B = 0. H' is the external field."""

        prefLabel = en("CoercivityBHcExternal")
        altLabel = pl("BH'c")

    class SwitchingFieldCoercivity(emmo.MagneticFieldStrength):
        """Defined by the maximum slope of the descending branch of
        the M-H hysteresis loop, with H the internal field."""

        comment = pl(
            "This field is often used when analysing the temperature\
            dependent coercivity for deriving microstructural parameters."
        )
        prefLabel = en("SwitchingFieldCoercivity")
        altLabel = pl("Hsw")

    class SwitchingFieldCoercivityExternal(emmo.MagneticFieldStrength):
        """Defined by the maximum slope of the descending branch of
        the M-H' hysteresis loop, with H' the external field."""

        prefLabel = en("SwitchingFieldCoercivityExternal")
        altLabel = pl("H'sw")

    class KneeField(emmo.MagneticFieldStrength):
        """The maximum working field - also named knee field H_K, is
        defined as the reverse internal field for which the magnetization
        is reduced by 10%; thus it corresponds to the point on the
        magnetization loop for which M = 0.9 Mr (J = 0.9 Jr)."""

        prefLabel = en("KneeField")
        altLabel = [
            en("KneeFieldInternal"),
            en("MaximumWorkingField"),
            pl("Hk"),
        ]

    class KneeFieldExternal(emmo.MagneticFieldStrength):
        """The maximum working field - also named knee field H_K,
        is defined as the reverse external field for which the
        magnetization is reduced by 10%; thus it corresponds to the
        point on the magnetization loop for which M = 0.9 Mr (J = 0.9 Jr).
        """

        prefLabel = en("KneeFieldExternal")
        altLabel = pl("H'k")

    class Remanence(emmo.ElectromagneticQuantity):
        """The remanence Mr which remains when the applied field is
        restored to zero in the hysteresis loop"""

        prefLabel = en("Remanence")
        altLabel = [
            enUS("RemanentMagnetization"),
            enGB("RemanentMagnetisation"),
            pl("Mr"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q4150950")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Remanence")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-40"
        )

    class RemanentMagneticPolarization(emmo.ElectromagneticQuantity):
        """The remanent magnetic polarization Jr which remains when the applied
        field is restored to zero in the hysteresis loop"""

        prefLabel = en("RemanentMagneticPolarization")
        altLabel = [
            enUS("RemanentMagneticPolarization"),
            enGB("RemanentMagneticPolarisation"),
            pl("Jr"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFluxDensityUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-02-39"
        )

    class ExternalSusceptibility(emmo.MagneticSusceptibility):
        """Ratio of the change of magnetization and the external
        field: M = chi' H'."""

        prefLabel = en("ExternalSusceptibility")
        altLabel = pl("chi'")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q691463")

    class InternalSusceptibility(emmo.MagneticSusceptibility):
        """Ratio of the change of magnetization and the internal
        field: M = chi H."""

        prefLabel = en("InternalSusceptibility")
        altLabel = pl("chi")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q691463")

    class MassSusceptibility(emmo.ElectromagneticQuantity):
        """Ratio of the change of the magnetic moment per unit mass and
        the internal field: sigma = chi_m H."""

        comment = en("magnetic susceptibility per mass density")
        prefLabel = en("MassSusceptibility")
        altLabel = pl("chi_m")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q104655916")
        is_a = [emmo.hasMeasurementUnit.some(emmo.VolumePerMassUnit)]

    class AbsolutePermeability(emmo.ElectromagneticQuantity):
        """Ratio of the change of magnetic flux density and the internal
        field: B = mu H."""

        prefLabel = en("AbsolutePermeability")
        altLabel = pl("mu")
        is_a = [emmo.hasMeasurementUnit.some(emmo.PermeabilityUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=121-12-28"
        )

    class MaximumEnergyProduct(emmo.ElectromagneticQuantity):
        """The value of the maximum energy product (BH)max is deduced from a
        plot of BH(B) for all points of the second quadrant of the B-H
        hysteresis loop. BH varies with B going through a maximum value (BH)max
        for a particular value of B.

        (BH)max equals the area of the largest second-quadrant rectangle which
        fits under the B-H loop.

        The maximum energy product is considered to be the best single index
        of quality of a permanent magnet material.
        It is twice the energy stored in the stray field of the magnet of
        optimal shape.
        """

        prefLabel = en("MaximumEnergyProduct")
        altLabel = pl("(BH)max")
        is_a = [emmo.hasMeasurementUnit.some(EnergyDensityUnit)]
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Maximum_energy_product")

    class SaturationMagneticPolarization(emmo.ElectromagneticQuantity):
        """The Saturation magnetic polarization Jsat is the maximum
        obtainable magnetic polarization for a given substance
        at a given temperature. Jsat should be used instead of Js to avoid
        confusion with the symbol for the spontaneous polarization"""

        prefLabel = en("SaturationMagneticPolarization")
        altLabel = [
            enUS("SaturationMagneticPolarization"),
            enGB("SaturationMagneticPolarisation"),
            en("Jsat"),
            en("Js"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFluxDensityUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-01-05"
        )

    class SaturationMagnetization(emmo.ElectromagneticQuantity):
        """The Saturation magnetization Msat is the maximum
        obtainable magnetic magnetization for a given substance
        at a given temperature. Msat should be used instead Ms to avoid
        confusion with the symbol for the SpontaneousMagnetization"""

        prefLabel = en("SaturationMagnetization")
        altLabel = [
            enUS("SaturationMagnetization"),
            enGB("SaturationMagnetisation"),
            en("Msat"),
            en("Ms"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.MagneticFieldStrengthUnit)]
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=221-01-04"
        )
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Saturation_(magnetic)")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q2630994")

    class LoopSquarenessFactorInternal(
        emmo.ElectromagneticQuantity, emmo.RatioQuantity
    ):
        """The internal loop squareness factor SF is defined as the ratio of
        the internal KneeField Hk over the internal Coercivity Hc
        (SF = KneeFieldInternal / CoercivityHcInternal)."""

        prefLabel = en("LoopSquarenessFactorInternal")
        altLabel = [
            en("SquarenessFactorInternal"),
            en("SF_internal"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit)]

    class LoopSquarenessFactorExternal(
        emmo.ElectromagneticQuantity, emmo.RatioQuantity
    ):
        """The external loop squareness factor is defined as the ratio of
        the external KneeField H'k over the external Coercivity H'c
        (SF' = KneeFieldExternal / CoercivityHcExternal)."""

        prefLabel = en("LoopSquarenessFactorExternal")
        altLabel = [
            en("SquarenessFactorExternal"),
            en("SF_external"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit)]

    class LoopSquareness(emmo.ElectromagneticQuantity, emmo.RatioQuantity):
        """The external loop squareness is defined as the ratio of
        the remanent polarisation over the saturation polarisation
        (SS = RemanentMagneticPolarization / SaturationMagneticPolarization)."""

        prefLabel = en("LoopSquareness")
        altLabel = [
            en("Squareness"),
            en("SS"),
        ]
        is_a = [emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit)]

    # -----------------------------------------------------

    class MagneticHysteresisProperties(emmo.Property):
        """The essential practical characteristic of any ferromagnetic material
        is the irreversible nonlinear response of magnetization M to an imposed
        magnetic field H. This response is given by the hysteresis loop. The
        characteristics of hysteresis loop are known as hysteresis properties.

        Instead of M(H), other quantities can be used to plot a hysteresis loop.

        M(H): Magnetization as function of the internal field.
        M(H'): Magnetization as function of the external field.

        J(H): Magnetic polarization as function of the internal field.
        J(H'): Magnetic polarization as function of the external field.

        B(H): Magnetic flux density as function of the internal field.
        B(H'): Magnetic flux density as function of the external field.
        """

        prefLabel = en("MagneticHysteresisProperties")
        is_a = [
            emmo.hasProperty.exactly(1, CoercivityHc),
            emmo.hasProperty.min(0, CoercivityBHc),
            emmo.hasProperty.min(0, CoercivityHcExternal),
            emmo.hasProperty.min(0, CoercivityBHcExternal),
            emmo.hasProperty.min(0, SwitchingFieldCoercivity),
            emmo.hasProperty.min(0, SwitchingFieldCoercivityExternal),
            emmo.hasProperty.min(0, KneeField),
            emmo.hasProperty.min(0, KneeFieldExternal),
            emmo.hasProperty.exactly(1, Remanence),
            emmo.hasProperty.min(0, RemanentMagneticPolarization),
            emmo.hasProperty.min(0, SaturationMagneticPolarization),
            emmo.hasProperty.min(0, LoopSquarenessFactorInternal),
            emmo.hasProperty.min(0, LoopSquarenessFactorExternal),
            emmo.hasProperty.min(0, LoopSquareness),
            emmo.hasProperty.min(0, MaximumEnergyProduct),
        ]

    class ExtrinsicMagneticProperties(emmo.Property):
        """Extrinsic magnetic Properties depend on the microstructure."""

        prefLabel = en("ExtrinsicMagneticProperties")
        is_a = [
            emmo.hasProperty.exactly(1, MagneticHysteresisProperties),
            emmo.hasProperty.min(0, DemagnetizingFactor),
            emmo.hasProperty.min(0, AbsolutePermeability),
            emmo.hasProperty.min(0, emmo.RelativePermeability),
        ]

    # -----------------------------------------------------

    # Magnet

    ## Microstructure

    class MainMagneticPhase(MagneticMaterial, emmo.PhaseOfMatter):
        """Main phase of the magnet"""

        prefLabel = en("MainMagneticPhase")
        is_a = [
            emmo.hasProperty.some(emmo.VolumeFraction),
            emmo.hasSpatialPart.exactly(
                1, AmorphousMagneticMaterial | CrystallineMagneticMaterial
            ),
        ]

    class SecondaryPhase(emmo.Material, emmo.PhaseOfMatter):
        """An additional phase within a magnet, for example soft inclusions
        or triple junctions."""

        prefLabel = en("SecondaryPhase")
        is_a = [
            emmo.hasProperty.some(emmo.VolumeFraction),
            emmo.hasSpatialPart.exactly(
                1,
                AmorphousMagneticMaterial
                | CrystallineMagneticMaterial
                | NonMagneticMaterial,
            ),
        ]

    class GrainBoundaryPhase(SecondaryPhase):
        """Material separating grains in a microstructure."""

        comment = en(
            "In permanent magnets, the grain boundary phase inhibits \
            the propagation of the magnetic reversal from grain to grain."
        )
        prefLabel = en("GrainBoundaryPhase")
        is_a = [
            emmo.hasProperty.some(emmo.Thickness),
        ]

    class GranularMicrostructure(emmo.Material):
        """The granular structure of a magnetic materials."""

        prefLabel = en("GranularMicrostructure")
        is_a = [
            emmo.hasSpatialPart.exactly(1, MainMagneticPhase),
            emmo.hasSpatialPart.min(0, SecondaryPhase),
            emmo.hasSpatialPart.min(0, GrainBoundaryPhase),
        ]

    class Magnet(emmo.FunctionalMaterial):
        """Piece of matter made of one or more magnetic materials."""

        prefLabel = en("Magnet")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q11421")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnet")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=151-14-06"
        )
        is_a = [
            emmo.hasProperty.min(0, emmo.MaterialsProcessing),
            emmo.hasProperty.min(0, emmo.WorkpieceForming),
            emmo.hasSpatialPart.min(0, GranularMicrostructure),
            emmo.hasProperty.exactly(1, ExtrinsicMagneticProperties),
            emmo.hasProperty.min(0, XrayDiffractionData),
        ]

    class BulkMagnet(Magnet, emmo.MaterialBySize):
        """Piece of matter made of one or more magnetic material."""

        prefLabel = en("BulkMagnet")
        is_a = [
            emmo.hasProperty.exactly(1, SampleGeometry),
            emmo.hasProperty.exactly(1, ShapeAnisotropy),
            emmo.hasProperty.exactly(1, DemagnetizingFactor),
        ]

    # local properties

    class Reflectivity(emmo.Property):
        """Capacity of an object to reflect light."""

        prefLabel = en("Reflectivity")
        altLabel = [
            en("Reflectance"),
            pl("R"),
        ]
        wikidataReference = pl("https://www.wikidata.org/wiki/Q663650")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Reflectance")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit),
        ]

    class LocalReflectivity(Reflectivity):
        """Local reflectivity measured with the magneto-optic Kerr effect."""

        prefLabel = en("LocalReflectivity")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalCoercivity(CoercivityHcExternal):
        """Local coercive field measured with the magneto-optic Kerr effect."""

        prefLabel = en("LocalCoercivity")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalXrayDiffractionData(XrayDiffractionData):
        """Local X-ray diffraction data."""

        prefLabel = en("LocalXrayDiffractionData")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalLatticeConstantA(LatticeConstantA):
        """The length of lattice vectors `a`, where lattice vectors
        `a`, `b` and `c` defines the unit cell, measured locally."""

        prefLabel = en("LocalLatticeConstantA")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalLatticeConstantC(LatticeConstantC):
        """The length of lattice vectors `c`, where lattice vectors
        `a`, `b` and `c` defines the unit cell, measured locally."""

        prefLabel = en("LocalLatticeConstantC")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalThickness(emmo.Thickness):
        """The thickness of the film measured locally."""

        prefLabel = en("LocalThickness")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalAtomPercent(emmo.RatioQuantity):
        """Local atomic percentage obtained from EDX quantification."""

        prefLabel = en("LocalAtomPercent")
        altLabel = [en("LocalAtomicPercent"), en("at.%")]
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.Percent),
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalMassPercent(emmo.RatioQuantity):
        """Local mass percentage obtained from EDX quantification."""

        prefLabel = en("LocalMassPercent")
        altLabel = [en("LocalWeightPercent"), en("wt.%")]
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.Percent),
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalAnnealingTemperature(emmo.ThermodynamicTemperature):
        """Local annealing temperature from heat treatment such as
        Rapid Thermal Annealing (RTA)."""

        prefLabel = en("LocalAnnealingTemperature")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalAnnealingTime(emmo.Duration):
        """Local annealing time (duration) from heat treatment such as
        Rapid Thermal Annealing (RTA)."""

        prefLabel = en("LocalAnnealingTime")
        altLabel = en("LocalAnnealingDuration")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalPhaseFraction(emmo.RatioQuantity):
        """Local phase fraction obtained from XRD analysis, typically
        expressed in weight percent."""

        prefLabel = en("LocalPhaseFraction")
        altLabel = en("LocalPhaseContent")
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.Percent),
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalEdxData(EdxData):
        """Local EDX data measured at a specific position."""

        prefLabel = en("LocalEdxData")
        altLabel = en("LocalEXDData")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalMokeData(MokeData):
        """Local MOKE data measured at a specific position."""

        prefLabel = en("LocalMokeData")
        altLabel = en("LocalMOKEData")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class LocalProfilometryData(ProfilometryData):
        """Local profilometry data measured at a specific position."""

        prefLabel = en("LocalProfilometryData")
        is_a = [
            emmo.hasProperty.exactly(1, emmo.PositionVector),
        ]

    class ThinFilmMagnet(Magnet, emmo.MaterialBySize):
        """Piece of matter made of one or more magnetic material
        in form a thin film."""

        prefLabel = en("ThinFilmMagnet")
        is_a = [
            emmo.hasProperty.min(0, InducedMagneticAnisotropy),
            emmo.hasProperty.min(0, SampleGeometry),
            emmo.hasProperty.min(0, LocalThickness),
            emmo.hasProperty.min(0, LocalCoercivity),
            emmo.hasProperty.min(0, LocalReflectivity),
            emmo.hasProperty.min(0, LocalXrayDiffractionData),
            emmo.hasProperty.min(0, LocalLatticeConstantA),
            emmo.hasProperty.min(0, LocalLatticeConstantC),
            # New properties from issue #20
            emmo.hasProperty.min(0, LocalAtomPercent),
            emmo.hasProperty.min(0, LocalMassPercent),
            emmo.hasProperty.min(0, LocalAnnealingTemperature),
            emmo.hasProperty.min(0, LocalAnnealingTime),
            emmo.hasProperty.min(0, LocalPhaseFraction),
            emmo.hasProperty.min(0, LocalEdxData),
            emmo.hasProperty.min(0, LocalMokeData),
            emmo.hasProperty.min(0, LocalProfilometryData),
            emmo.hasProperty.min(0, Xrd2dImage),
        ]

    # Magnetic multilayers

    ## Magnetotransport

    class Magnetoresistance(emmo.RatioQuantity):
        """Change of the resistivity of a substance due to an applied
        magnetic field.

        Magnetoresistance can be defined as MR = [ϱ(B)-ϱ(0)]/ϱ(0).
        """

        prefLabel = en("Magnetoresistance")
        altLabel = pl("MR")
        wikidataReference = pl("https://www.wikidata.org/wiki/Q58347")
        wikipediaReference = pl("https://en.wikipedia.org/wiki/Magnetoresistance")
        IECEntry = pl(
            "https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=121-12-83"
        )
        is_a = [
            emmo.hasMeasurementUnit.some(emmo.DimensionlessUnit),
        ]

    class SpacerLayer(emmo.Material):
        """Nonmagnetic thin film materials."""

        prefLabel = en("SpacerLayer")
        is_a = [
            Not(MagneticMaterial),
            emmo.hasProperty.exactly(1, emmo.ChemicalComposition),
            emmo.hasProperty.some(emmo.Thickness),
        ]

    class StackingSequence(emmo.NominalProperty):
        """Sequence of layers in a multilayer stack."""

        prefLabel = en("StackingSequence")
        is_a = [emmo.hasStringValue.some(emmo.String)]

    class MultilayerMagnet(emmo.SpatialTiling, Magnet):
        """Piece of matter made of stacked layers of one or more magnetic
        materials."""

        prefLabel = en("MultilayerMagnet")
        is_a = [
            emmo.hasSpatialTile.some(ThinFilmMagnet),
            emmo.hasSpatialTile.min(0, SpacerLayer),
            emmo.hasProperty.exactly(1, SampleGeometry),
            emmo.hasProperty.exactly(1, StackingSequence),
            emmo.hasProperty.min(0, Magnetoresistance),
        ]


onto.sync_attributes(
    name_policy="uuid", class_docstring="elucidation", name_prefix="EMMO_"
)

#################################################################
# Annotate the ontology metadata
#################################################################
onto.metadata.comment.append(
    "Created within the EU project MaMMoS. Grant number 101135546 \
    (HORIZON-CL4-2023-DIGITAL-EMERGING-01)."
)

onto.metadata.abstract.append(
    en(
        "An EMMO-based domain-ontology for magnetic materials."
        "Created within the EU project MaMMoS."
        "Grant number 101135546 (HORIZON-CL4-2023-DIGITAL-EMERGING-01)."
        "The Magnetic Materials Ontology is released under the Creative Commons "
        "Attribution 4.0 International license (CC BY 4.0)."
    )
)

onto.metadata.title.append(en("Magnetic Materials Ontology"))
onto.metadata.creator.append(en("Wilfried Hortschitz"))
onto.metadata.creator.append(en("Thomas Schrefl"))
onto.metadata.creator.append(en("Santa Pile"))
onto.metadata.contributor.append(en("William Rigaut"))
onto.metadata.contributor.append(en("Andrea Petrocchi"))
onto.metadata.contributor.append(en("Martin Lang"))
onto.metadata.contributor.append(en("Sam Holt"))
onto.metadata.contributor.append(en("Swapneel Amit Pathak"))
onto.metadata.contributor.append(en("Hans Fangohr"))
onto.metadata.contributor.append(en("Jonas Winkler"))
onto.metadata.versionInfo.append(en(__version__))
onto.metadata.comment.append(
    en(
        "Contacts:\n"
        "Wilfried Hortschitz\n"
        "DISS-UWK\n"
        "email: wilfried.hortschitz@donau-uni.ac.at\n"
    )
)

# set version of ontology
onto.set_version(str(__version__))
onto.save("magnetic-materials.ttl", overwrite=True)
# world.save()
