"""
Tests for straight_line module

Copyright (c) Andrew R. McCluskey and Benjamin J. Morgan

Distributed under the terms of the MIT License

@author: Andrew R. McCluskey
"""

# pylint: disable=R0201

import unittest
from unittest.mock import patch
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
from uncertainties import ufloat
from kinisi import straight_line


class TestStraightLine(unittest.TestCase):
    """
    Unit tests for straight_line module
    """
    @patch('numpy.random.uniform', return_value=np.ones(5))
    def test_prior(self, mocked):
        """
        Test prior function using mock.
        """
        initial_guess = 10
        actual_prior = straight_line.prior(initial_guess, 5)
        mocked.assert_called_with(-90, 110, 5)
        assert_almost_equal(actual_prior, np.ones(5) * 1)

    def test_comparison(self):
        """
        Test comparison function.
        """
        gradient = 0
        intercept = 1.1
        y_data = np.ones(10)
        dy_data = np.ones(10) * 0.1
        expected_lnl = 8.8364655979
        actual_lnl = straight_line.comparision(
            (gradient, intercept),
            y_data,
            dy_data,
            np.linspace(0, 9, 10),
        )
        assert_almost_equal(actual_lnl, expected_lnl)

    def test_run_sampling(self):
        """
        Test the run sampling function.
        """
        y_data = np.ones(10)
        dy_data = np.ones(10) * 0.1
        x_data = np.linspace(0, 9, 10)
        init_guesses = (ufloat(0., 0.), ufloat(1.1, 0))
        samples = straight_line.run_sampling(
            init_guesses,
            y_data,
            dy_data,
            x_data,
            n_samples=5,
            n_burn=5,
            progress=False,
        )
        assert_equal(samples.shape, (500, 2))
