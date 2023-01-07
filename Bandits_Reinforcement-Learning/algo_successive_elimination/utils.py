"""Successive elimination algorithm: binomial rewards.

This is a stochastic bandit problem, where the reward for each arm have a
binomial distribution: binomial(bin_n,p_a), where bin_n is chosen and p_a is
randomly generated for each arm 'a'.
"""

import numpy as np
from numpy.random import binomial, uniform


class SuccessiveElimination:
    """Successive elimination algorithm."""

    def __init__(self, n_arms, bin_n, T, delta):
        """Initialize the class.

        n_arms: number of arms
        bin_n: binomial distribution hyperparameter
        T: total number of iterations
        delta: upper confidence bound probability
        """
        self.active_arms = np.ones(n_arms, dtype=bool)
        self.binomial_parameters = [(bin_n, uniform()) for _ in range(n_arms)]
        self.visited_arms = np.zeros(n_arms, dtype=int)
        self.empirical_mean = np.zeros(n_arms)
        self.delta = delta
        self.T = T

    def ucb(self, arm):
        """Upper confidence bound."""
        return self.empirical_mean[arm] + np.sqrt(
            2 * np.log(1 / self.delta) / self.visited_arms[arm]
        )

    def lcb(self, arm):
        """Lower confidence bound."""
        return self.empirical_mean[arm] - np.sqrt(
            2 * np.log(1 / self.delta) / self.visited_arms[arm]
        )

    def run(self):
        """Run the algorithm."""
        while sum(self.active_arms) > 1 and self.T > 0:

            for arm in np.where(self.active_arms)[0]:
                self.visited_arms[arm] += 1
                self.empirical_mean[arm] += (
                    binomial(
                        self.binomial_parameters[arm][0],
                        self.binomial_parameters[arm][1],
                    )
                    / self.binomial_parameters[arm][0]
                )
            for arm in np.where(self.active_arms)[0]:
                ucb = self.ucb(arm)
                for arm_ in np.where(self.active_arms)[0]:
                    if self.lcb(arm_) > ucb:
                        self.active_arms[arm] = False
                        continue

            self.T -= 1
