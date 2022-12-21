"""Notebook for the phased successive elimination algorithm."""

from utils import PhasedSuccessiveElimination


# Parameters
n_arms = 10
bin_n = 500
phases = 4
arm_repetition = 10

# Algorithm
algo_se = PhasedSuccessiveElimination(n_arms, bin_n, phases, arm_repetition)

algo_se.run()

algo_se.empirical_mean
algo_se.active_arms

algo_se.binomial_parameters
