"""
The two classes herein enable the determination of the activation energy from
a diffusion-Arrhenius or -Super-Arrhenius plot.
This includes the uncertainty on the activation energy from the MCMC sampling
of the plot, with uncertainties on diffusion.
Furthermore, the classes are build on the Relationship subclass, therefore
it is easy to determine the Bayesian evidence for each of the models with the
given data, enabling the distinction between Arrhenius and Super-Arrhenius
diffusion.
"""

# Copyright (c) Andrew R. McCluskey and Benjamin J. Morgan
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey

# pylint: disable=R0913

import sys
import numpy as np
from uravu.distribution import Distribution
from uravu.relationship import Relationship
from scipy.constants import R
from scipy.stats import uniform
from uravu import UREG


class StandardArrhenius(Relationship):
    r"""
    Evaluate the data with a standard Arrhenius relationship.

    Attributes:
        activation_energy (uncertainties.ufloat or
            kinisi.distribution.Distribution): The value and associated
            uncertainty for the activation energy from the standard
            Arrhenius relationship. The uncertainty is initially obtained
            from a weighted least squares fit, the accuracy of this can
            be improved by using the `sample()` method. The unit is eV.
    """
    def __init__(self, temperature, diffusion, diffusion_error,
                 temperature_unit=UREG.kelvin,
                 diffusion_unit=UREG.centimeter**2 / UREG.second,
                 temperature_names=r'$T$',
                 diffusion_names=r'$D$', unaccounted_uncertainty=False):
        """
        Args:
            temperature (array_like): The temperature data.
            diffusion (array_like): The diffusion coefficient data.
            diffusion_error (array_like): The uncertainty in the diffusion
                coefficient data.
            temperature_unit (pint.UnitRegistry(), optional): The unit for
                the temperature. Default is kelvin.
            diffusion_unit (pint.UnitRegistry(), optional): The unit for
                the diffusion coefficient. Default is centimetre**2 per
                second.
            temperature_names (str): The label for the temperature. Default is
                `$T$`.
            diffusion_names (str): The label for the diffusion coefficient.
                Default is `$D$`.
        """
        variable_names = [r'$E_a$', r'$A$']
        variable_units = [UREG.joules / UREG.mole, UREG.dimensionless]
        if unaccounted_uncertainty:
            variable_names.append('unaccounted uncertainty')
            variable_units.append(UREG.dimensionless)
        super().__init__(
            arrhenius, temperature, diffusion, diffusion_error, temperature_unit,
            diffusion_unit, temperature_names, diffusion_names, variable_names, variable_units, unaccounted_uncertainty)

    def all_positive_prior(self):
        """
        This creates an all positive prior.
        """
        priors = []
        for var in self.variable_medians:
            loc = sys.float_info.min
            scale = (var + np.abs(var) * 2) - loc
            priors.append(uniform(loc=loc, scale=scale))
        if self.unaccounted_uncertainty:
            priors[-1] = uniform(loc=-10, scale=11)
        return priors

    def sample(self, **kwargs):
        """
        Use MCMC to sample the posterior distribution of the relationship.
        """
        self.mcmc(prior_function=self.all_positive_prior, **kwargs)

    def nested(self, **kwargs):
        """
        Use nested sampling with all positive prior
        """
        self.nested_sampling(prior_function=self.all_positive_prior, **kwargs)


def arrhenius(abscissa, activation_energy, prefactor):
    """
    Determine the diffusion coefficient for a given activation energy, and
    prefactor according to the Arrhenius equation.

    Args:
        abscissa (array_like): The abscissa data.
        activation_energy (float): The activation_energy value.
        prefactor (float): The prefactor value.

    Returns:
        array_line: The diffusion coefficient data.
    """
    return prefactor * np.exp(-1 * activation_energy / (R * abscissa))


class SuperArrhenius(Relationship):
    """
    Evaluate the data with a Super-Arrhenius relationship.

    Attributes:
        activation_energy (uncertainties.ufloat or
            kinisi.distribution.Distribution): The value and associated
            uncertainty for the activation energy from the
            Super-Arrhenius relationship. The uncertainty is initially
            obtained from a weighted least squares fit, the accuracy of this
            can be improved by using the `sample()` method. The unit is eV.
    """
    def __init__(self, temperature, diffusion, diffusion_error,
                 temperature_unit=UREG.kelvin,
                 diffusion_unit=UREG.centimeter**2 / UREG.second,
                 temperature_names=r'$T$',
                 diffusion_names=r'$D$', unaccounted_uncertainty=False):
        """
        Args:
            temperature (array_like): The temperature data.
            diffusion (array_like): The diffusion coefficient data.
            diffusion_error (array_like): The uncertainty in the diffusion
                coefficient data.
            temperature_unit (pint.UnitRegistry(), optional): The unit for
                the temperature. Default is kelvin.
            diffusion_unit (pint.UnitRegistry(), optional): The unit for
                the diffusion coefficient. Default is centimetre**2 per
                second.
            temperature_names (str): The label for the temperature. Default is
                `$T$`.
            diffusion_names (str): The label for the diffusion coefficient.
                Default is `$D$`.
        """
        variable_names = [r'$E_a$', r'$A$', r'$T_0$']
        variable_units = [UREG.joules / UREG.mole, UREG.dimensionless, UREG.kelvin]
        if unaccounted_uncertainty:
            variable_names.append('unaccounted uncertainty')
            variable_units.append(UREG.dimensionless)
        super().__init__(
            super_arrhenius, temperature, diffusion, diffusion_error, temperature_unit,
            diffusion_unit, temperature_names, diffusion_names, variable_names, variable_units, unaccounted_uncertainty)

    def all_positive_prior(self):
        """
        This creates an all positive prior.
        """
        priors = []
        loc = sys.float_info.min
        for var in self.variable_medians:
            scale = (var + np.abs(var) * 4) - loc
            priors.append(uniform(loc=loc, scale=scale))
        if self.unaccounted_uncertainty:
            if self.variable_medians[-2] == 0:
                self.variable_medians[-2] = 1
            priors[-2] = uniform(loc=loc, scale=np.sort(self.abscissa.m)[0] - 0.1)
            priors[-1] = uniform(loc=-10, scale=11)
        else:
            if self.variable_medians[-1] == 0:
                self.variable_medians[-1] = 1
            priors[-1] = uniform(loc=loc, scale=np.sort(self.abscissa.m)[0] - 0.1)
        return priors

    def sample(self, **kwargs):
        """
        Use MCMC to sample the posterior distribution of the relationship.
        """
        self.mcmc(prior_function=self.all_positive_prior, **kwargs)

    def nested(self, **kwargs):
        """
        Use nested sampling with all positive prior
        """
        self.nested_sampling(prior_function=self.all_positive_prior, **kwargs)

def super_arrhenius(abscissa, activation_energy, prefactor, t_zero):
    """
    Determine the rate constant for a given activation energy, prefactor,
    and t_zero according to the Vogel–Tammann–Fulcher equation.

    Args:
        abscissa (array_like): The abscissa data.
        activation_energy (float): The activation_energy.
        prefactor (float): The prefactor.
        t_zero (float): The T_0 value.

    Returns:
        array_line: The ordinate data.
    """
    return prefactor * np.exp(
        -1 * activation_energy / (R * (abscissa - t_zero)))
