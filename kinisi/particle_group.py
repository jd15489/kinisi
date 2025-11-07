"""
ParticleGroup class for kinisi. This module contains a single class, whose purpose is to hold information about a single group of particles to be analysised.
"""

# Copyright (c) kinisi developers.
# Distributed under the terms of the MIT Lisense.
# author: Josh Dunn (jd15489), Andrew R. McCluskey (arm61), Harry Richardson (Harry-Rich) and Oskar G. Soulas (osoulas).

import importlib

import numpy as np
import scipp as sc
from scipp.typing import VariableLikeType

from kinisi import __version__

from .due import Doi, due

class ParticleGroup(sc.DataGroup):
    """
    :parm coords: an array with dimensions `time`, `particle`, `dimension`
    """
    def __init__(self,
                 indices: VariableLikeType,
                 coords: VariableLikeType = None,
                 masses: VariableLikeType = None,
                 charge: VariableLikeType = None,
                 charges: VariableLikeType = None,
                ):
        super().__init__(
            indices = indices,
            coords = coords,
            masses = masses,
            charge = charge,
            charges = charges,
        )
        
    def get_molecules(self):
        """
        """

    
    def get_COMs(self):
        "Alias for get_molecules"
        self.get_molecules()