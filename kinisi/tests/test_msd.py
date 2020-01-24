"""
Tests for msd module

Copyright (c) Andrew R. McCluskey and Benjamin J. Morgan

Distributed under the terms of the MIT License

@author: Andrew R. McCluskey
"""

# pylint: disable=R0201

import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from kinisi.msd import MSD


class TestMsd(unittest.TestCase):
    """
    Unit tests for utils module
    """
    def test_msd_init_a(self):
        """
        Test the initialisation of the MSD class with defaults.
        """
        sq_disp = [np.ones((i, i+1)) for i in range(1, 6)[::-1]]
        msd = MSD(sq_disp, np.linspace(1, 100, len(sq_disp)))
        for i, disp in enumerate(sq_disp):
            assert_almost_equal(msd.sq_displacements[i], disp)
        assert_equal(msd.mean, np.ones((5)))
        num_part = np.array([(i * (i+1)) for i in range(1, 6)[::-1]])
        assert_equal(msd.err, np.sqrt(6 / num_part))

    def test_msd_init_b(self):
        """
        Test the initialisation of the MSD class without defaults.
        """
        sq_disp = [np.ones((i, i+1)) for i in range(1, 6)[::-1]]
        msd = MSD(sq_disp, np.linspace(1, 100, len(sq_disp)), step_freq=2)
        expected_sq_disp = sq_disp[::2]
        for i, disp in enumerate(expected_sq_disp):
            assert_almost_equal(msd.sq_displacements[i], disp)
        assert_equal(msd.mean, np.ones((3)))
        num_part = np.array([(i * (i+1)) for i in range(1, 6)[::-2]])
        assert_equal(msd.err, np.sqrt(6 / num_part))

    def test_resample(self):
        """
        Test bootstrap with default confidence intervals.
        """
        data = [np.ones((5, 5))] * 5
        msd = MSD(data, np.linspace(1, 10, 5))
        msd.resample()
        assert_equal(msd.mean.size, 5)
        assert_equal(msd.err.size, 5)
        assert_equal(msd.resampled, True)
