"""UCB1 algorithms: binomial rewards.

This is a stochastic bandit problem, where the reward for each arm have a
binomial distribution: binomial(bin_n,p_a), where bin_n is chosen and p_a is
randomly generated for each arm 'a'.
"""

import numpy as np
from numpy.random import binomial, uniform


class UCB1:
    """UCB1 algorithm."""

    def __init__(self, n_arms, bin_n, T, delta):
        """Initialize the class.

        n_arms: number of arms
        bin_n: binomial distribution hyperparameter
        T: total number of iterations
        delta: upper confidence bound probability
        """
        self.binomial_parameters = [(bin_n, uniform()) for _ in range(n_arms)]
        self.visited_arms = np.zeros(n_arms, dtype=int)
        self.empirical_mean = np.zeros(n_arms)
        self.delta = delta
        self.T = T
        self.arms = n_arms
        self.reward_path = []
        self.arm_path = []

    def ucb(self, arm):
        """Upper confidence bound."""
        return self.empirical_mean[arm] + np.sqrt(
            2 * np.log(1 / self.delta) / self.visited_arms[arm]
        )

    def run(self):
        """Run the algorithm."""

        for arm in range(self.arms):

            reward = (
                binomial(
                    self.binomial_parameters[arm][0],
                    self.binomial_parameters[arm][1],
                )
                / self.binomial_parameters[arm][0]
            )
            self.empirical_mean[arm] += reward
            self.visited_arms[arm] += 1
            self.arm_path.append(arm)
            self.reward_path.append(reward)

        for _ in range(self.T):

            arms_ucb = [self.ucb(arm) for arm in range(self.arms)]
            arm_max = np.argmax(arms_ucb)
            reward = (
                binomial(
                    self.binomial_parameters[arm_max][0],
                    self.binomial_parameters[arm_max][1],
                )
                / self.binomial_parameters[arm_max][0]
            )
            self.empirical_mean[arm_max] += reward
            self.visited_arms[arm_max] += 1
            self.arm_path.append(arm_max)
            self.reward_path.append(reward)
