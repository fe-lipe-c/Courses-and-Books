"""Notebook for the successive elimination algorithm."""

from utils import SuccessiveElimination
import altair as alt

# Parameters
n_arms = 10
bin_n = 500
T = 100
delta = 0.4

# Algorithm
algo_se = SuccessiveElimination(n_arms, bin_n, T, delta)

algo_se.run()

algo_se.empirical_mean
algo_se.T
algo_se.visited_arms
algo_se.active_arms

algo_se.binomial_parameters
