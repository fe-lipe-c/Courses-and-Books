# An Introduction to Auction Theory

## Chapter 2: Preliminaries

### Bayesian Nash Equilibrium

We can think of games of incomplete information as a two-stage game. Prior to the beginning of the game, before players make a decision, nature chooses a type for each player. At this stage, each player knows his own type but not the types of other players. In the second stage, each player chooses a strategy knowing his own type and the initial distribution of all types.

The set of players will be denoted by $I = \left\{1,2,\dots,n \right\}$. The set of possible types for each player $i \in I$ is denoted by $X_{i}$. We denote by $F (\cdot)$ the probability distribution over $X = X_{1} \times X_{2} \times \cdots \times X_{n}$, which reflects the probabilities attached to each combination of types occurring.

We denote by $S_{i}$ the set of strategies for player $i \in I$ and by $s_{i}: X_{i} \to S_{i}$ the decision function of player $i$. We denote by $\hat{F}_{i}(x_{-i}|x_{i})$ the probability distribution of types $x_{-i}$ of players $j \neq i$ given that $i$ knows his type is $x_{i}$. That is, player $i$ updates his prior information about the distribution of the other types using Bayes rule upon learning that his type is $x_{i}$.

We let $\pi_{i}(s_{i},s_{-i},x_{i},x_{-i})$ denote $i$'s profits given that his type is $x_{i}$, that he chooses $s_{i} \in S_{i}$ and that th other players follow strategies $s_{-i}(x_{-i}) = (s_{j}(x_{j}))_{j\neq i}$ ant their types are $x_{-i}$. For each vector $(x_{1},x_{2},\dots,x_{n})$ chosen by nature, there are updated beliefs given by $\hat{F}_{1}(x_{-1}|x_{1}), \dots, \hat{F}_{n}(x_{-n}|x_{n})$.

A Bayesian Game is defined as a five-tuple
$$
\begin{equation*}
	G = \left[I, \left\{S_{i}\right\}_{i \in I}, \left\{\pi_{i}(\cdot) \right\}_{i \in I}, X, F (\cdot)\right]
\end{equation*}
$$
That is, it is a set of players, a strategy set for each player, a payoff (or utility) function for each player, a set of possible types and a distribution over the set of types.

A Bayesian Nash Equilibrium is a list of decision functions $\left(s_{1}^{*}(\cdot),\dots, s_{n}^{*}(\cdot)\right)$, such that 
