# pylint: disable=wrong-import-position
"""
pyIPCS Exports
"""

import sys

if sys.platform != "zos":
    raise RuntimeError("This package is only supported on z/OS.")

from ._version import __version__
from . import exceptions
from . import driver
from . import ipcs
from .dump import IpcsDump
from .ddir import IpcsDdir
from .response import TsoResponse, IpcsResponse, IpcsParsedResponse

__all__ = [
    "__version__",
    "exceptions",
    "driver",
    "ipcs",
    "IpcsDump",
    "IpcsDdir",
    "TsoResponse",
    "IpcsResponse",
    "IpcsParsedResponse",
]
