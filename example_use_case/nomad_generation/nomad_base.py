from typing import (
  TYPE_CHECKING,
)

import numpy as np
from nomad.datamodel.data import (
  ArchiveSection,
  EntryData,
)
from nomad.metainfo import (
  Package,
  Quantity,
  Section,
  SubSection,
)

if TYPE_CHECKING:
  from nomad.datamodel.datamodel import (
      EntryArchive,
  )
  from structlog.stdlib import (
      BoundLogger,
  )

m_package = Package(name='Schema for Mammos')
m_package.__init_metainfo__()

def Length():
  return Quantity(
      type=np.float64,
      a_eln={
          "component": "NumberEditQuantity",
          "defaultDisplayUnit": "nm"
      },
      unit="nm",
  )

def Angle():
  return Quantity(
      type=np.float64,
      a_eln={
          "component": "NumberEditQuantity",
          "defaultDisplayUnit": "rad"
      },
      unit="rad",
  )

def EnergyDensity():
  return Quantity(
      type=np.float64,
      a_eln={
          "component": "NumberEditQuantity",
          "defaultDisplayUnit": "MJ/m**3"
      },
      unit="J/m**3",
  )

def Volume():
  return Quantity(
      type=np.float64,
      a_eln={
          "component": "NumberEditQuantity",
          "defaultDisplayUnit": "nm**3"
      },
      unit="nm**3",
  )
