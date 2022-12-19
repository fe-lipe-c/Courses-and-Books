# Theory  of Multi-armed Bandits and Reinforcement Learning

### Lecture 01: Introduction to Bandits and Reinforcement Learning

#### Multi-armed Bandits

- Types: stochastic, contextual, adversarial
- Feedback model: 
	1. Bandit feedback: only the reward corresponding to the selected action is revealed.
	2. Partial feedback: some additional information about the rewards linked to unchosen actions is revealed.
	3. Full feedback: rewards linked to all actions that could have been chosen are revealed.

#### Reinforcement Learning

Can be viewed as a generalization of the bandits setting.

**Comment:** Reinforcement learning can be seen as a generalization of bandits because, while the latter is seen as an algorithm for one-step problems, the former is for sequential problems. Another perspective is to see bandits being applied to problems where the agent's action does not interfere with the next state, while RL modifies, through action, the dynamics of the system. Example: an agent who trades on the stock market several times within a time frame can interfere with market dynamics if the asset being traded is illiquid; otherwise, if the stock is very liquid and the amount traded by the agent is minimal, within a reasonable time frame, the market dynamics are unchanged.

### Lecture 02: Analysis of finite-arm i.i.d.-reward bandit

#### Notation

![bandit_notation](img/bandit_notation.png)

#### Finite-arm i.i.d. Reward Bandit
#### Designing Algorithms to Minimize Regret

**Definition 1 (Best Arm Benchmark).**  Always playing the optimal arm every round is the best outcome for the learner and results in the best performance for the game. Denote the expected reward of the optimal arm as $\mu^{*}$. We call $T \cdot \mu^{*}$ the best arm benchmark.

**Definition 2 (Random Regret).** Random regret is defined as the difference between the best arm benchmark and our cumulative reward during the game:
$$
\begin{equation*}
	T\mu^{*} - \sum_{t=1}^{T} X_{t} \tag{1}
\end{equation*}
$$

**Definition 3 (Pseudo Regret).** Pseudo regret is the difference between the best arm benchmark and the sum of the expected rewards of each arm played:
$$
\begin{equation*}
	R(T) = T\mu^{*} - \sum_{t=1}^{T} \mu_{A_{t}} \geq 0 \tag{2}
\end{equation*}
$$

**Definition 4 (Worst Case Expected Regret).** Worst case expected regret is defined as the worst-case expected pseudo regret:
$$
\begin{equation*}
	\sup_{\mu_{1}, \mu_{2}, \dots, \mu_{K}} \mathbb{E}[R(T)] \tag{3}
\end{equation*}
$$

#### The Explore-then-Commit Algorithm and its Analysis

![explore_then_commit](img/algo_exp_commit.png)

**Theorem 5 (Hoeffding's Inequality)** Let $X_{1}, X_{2}, X_{3}, \dots \stackrel{i.i.d.}{\sim} P, \mathbb{E}[X_{i}] = \mu$ and $X_{i} \in [0,1]$ with probability 1. Then
$$
\begin{equation*}
	\mathbb{P} \left(\left|\frac{1}{n}\sum_{i=1}^{n}X_{i}-\mu \right| \geq \epsilon \right) \leq 2 \exp \{-2n\epsilon^{2}\}
\end{equation*}
$$
Hoeffding's inequality belongs to a broad class of inequalities, called concentration inequalities.

**Theorem 6.** With $N = (T / K)^{2/3}(\ln T)^{1/3}$, Algorithm 1 achieves worst-case expected regret bound $\mathbb{E}[R (T)] \leq O (T^{2/3}(K \ln T)^{1/3})$.

It is interesting to see that, with such a naive algorithm, the regret bound is sublinear with respect to $T$.

### Lecture 03: Explore then commit and successive elimination
