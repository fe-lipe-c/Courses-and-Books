"""Notebook for the explore-then-commit algorithm."""

from numpy.random import binomial, uniform
import numpy as np
import pandas as pd
import altair as alt

# We'll model each arms' reward by a binomial distribution.

n_arms = 10
n = 5
binomial_parameters = [(n, uniform()) for i in range(n_arms)]

steps = 1000
exploration_par = 0.1

reward_path = np.zeros(n_arms)

for t in range(steps):

    while t <= int(exploration_par * steps):
        # Explore
        for arm in range(n_arms):
            reward_path[arm] += (
                binomial(binomial_parameters[arm][0], binomial_parameters[arm][1]) / n
            )

        t += 1

    # Commit
    best_arm = np.argmax(reward_path)

best_arm
binomial_parameters
