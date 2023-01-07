"""Notebook for the UCB1 algorithm."""

from utils import UCB1

# Parameters
n_arms = 100
bin_n = 50
T = 10000
delta = 1 / T

# Algorithm
algo_se = UCB1(n_arms, bin_n, T, delta)

algo_se.run()

algo_se.empirical_mean
algo_se.visited_arms

algo_se.binomial_parameters
