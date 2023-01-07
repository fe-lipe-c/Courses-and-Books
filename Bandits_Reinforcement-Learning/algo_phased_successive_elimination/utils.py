"""Phased Successive elimination algorithm: binomial rewards.

This is a stochastic bandit problem, where the reward for each arm have a
binomial distribution: binomial(bin_n,p_a), where bin_n is chosen and p_a is
randomly generated for each arm 'a'.
"""

import numpy as np
from numpy.random import binomial, uniform


class PhasedSuccessiveElimination:
    """Phased Successive elimination algorithm."""

    def __init__(self, n_arms, bin_n, phases, arm_repetition):
        """Initialize the class.

        n_arms: number of arms
        bin_n: binomial distribution hyperparameter
        phases: number of phases
        arm_repetition: number of repetitions for each arm at each phase
        """
        self.active_arms = np.ones(n_arms, dtype=bool)
        self.binomial_parameters = [(bin_n, uniform()) for _ in range(n_arms)]
        self.empirical_mean = np.zeros(n_arms)
        self.phases = phases
        self.arm_repetition = arm_repetition

    def run(self):
        """Run the algorithm."""
        # while sum(self.active_arms) > 1 and self.T > 0:
        for _ in range(self.phases):

            for arm in np.where(self.active_arms)[0]:
                for _ in range(self.arm_repetition):
                    reward = (
                        binomial(*self.binomial_parameters[arm])
                        / self.binomial_parameters[arm][0]
                    )
                    self.empirical_mean[arm] += reward

            max_arm = np.argmax(self.empirical_mean)
            for arm in np.where(self.active_arms)[0]:
                delta_mean = self.empirical_mean[arm] + 2 ** (-self.phases)
                if delta_mean < self.empirical_mean[max_arm]:
                    self.active_arms[arm] = False
