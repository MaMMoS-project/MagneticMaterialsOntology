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
