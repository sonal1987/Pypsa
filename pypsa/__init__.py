# -*- coding: utf-8 -*-
"""
Python for Power Systems Analysis (PyPSA)

Grid calculation library.
"""

from pypsa import (
    components,
    contingency,
    descriptors,
    examples,
    geo,
    io,
    linopf,
    linopt,
    networkclustering,
    opf,
    opt,
    optimization,
    pf,
    plot,
)
from pypsa.components import Network, SubNetwork

__version__ = "0.22.1"

__author__ = (
    "PyPSA Developers, see https://pypsa.readthedocs.io/en/latest/developers.html"
)
__copyright__ = (
    "Copyright 2015-2023 PyPSA Developers, see https://pypsa.readthedocs.io/en/latest/developers.html, "
    "MIT License"
)
