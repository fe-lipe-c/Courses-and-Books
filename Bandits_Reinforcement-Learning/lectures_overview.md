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

##### Notation

![bandit_notation](img/bandit_notation.png)

##### 2.1 Finite-arm i.i.d. Reward Bandit

This is a basic model of the bandit problem with i.i.d. rewards. There are two properties for this problem:
1. It is memoryless, meaning the reward after round $t$ does not depend on any action or reward before round $t$ once the action at round $t$ is given: $\mathbb{P}_{X_{t}|A_{1},X_{1}, A_{2},X_{2}, \dots, X_{t-1},A_{t}} = \mathbb{P}_{A_{t}}$.
2. It is casual, meaning that the action of the learner during round $T$ is influenced by the actions and rewards of previous rounds: $\mathbb{P}_{A_{t}|A_{1},X_{1}, A_{2},X_{2}, \dots,A_{t-1}, X_{t-1}} = \pi_{t}(\cdot | A_{1},X_{1}, A_{2},X_{2},\dots,A_{t-1},X_{t-1})$.

##### 2.2 Designing Algorithms to Minimize Regret

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

##### 2.3 The Explore-then-Commit Algorithm and its Analysis

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

**Definition (Clean Event)** The case when every empirical mean $\bar{\mu}(a)$ stays close to the true expectation $\mu (a)$, and provide a lower bound for $\mathbb{P}(\mathcal{E})$ using Hoeffding's inequality. 

### Lecture 03: Explore then commit and successive elimination

##### 3.2 Adaptive Exploration vs Non-Adaptive Exploration

**Adaptive Exploration:** the choice of next arm depends on the reward history. \
**Non-adaptive Exploration:** pull every arm the same number of times which has been specified without seeing the reward.

**Definition 1.** The true expected reward of bandit arm $a$ is $\mu_{a} = \mu (a) = \mathbb{E}_{\sim \mathbb{P}_{a}}[R_{a,i}]$, for every $i \in [0,T]$.

**Definition 2.** At time $t$, the number of times arm $a$ has been pulled is $n_{t}(a)$.

**Definition (Empirical Average Reward)** The empirical average reward of arm $a$, at time $t$, is:
$$
\begin{equation*}
	\bar{\mu}_{t}(a) = \frac{1}{n_{t}(a)} \sum_{i=1}^{n_{t}(a)} R_{a,i} 
\end{equation*}
$$

**Theorem 3.** Under the setting of Adaptive Exploration, assume we pulled arm $a$ $n_{t}(a)$ times:
$$
\begin{equation*}
	\mathbb{P}\left(|\bar{\mu}(a) - \mu (a)| \leq r_{t}(a)\right) \geq 1 - \frac{1}{T^{4}}
\end{equation*}
$$
where $r_{t}(a) = \sqrt{\frac{2 \log (T)}{n_{t}(a)}}$.

We can no longer apply the Hoeffding's inequality here since it assumes that the sample is drawn independently from a distribution with a fixed number of times.

##### 3.3 Successive Elimination

**Definition 4.**  
Upper Confidence Bound: $\text{UCB}_{t}(a) = \bar{\mu}_{t}(a) + r_{t}(a)$

Lower Confidence Bound: $\text{LCB}_{t}(a) = \bar{\mu}_{t}(a) - r_{t}(a)$


![successive_elimination](img/successive_elimination.png)

**Theorem 5.** Under The setting of successive elimination, the pseudo-regret
$$
\begin{equation*}
	R (T) \precsim \sqrt{KT \log (T)}
\end{equation*}
$$


### Lecture 04: Analysis of Successive Elimination and UCB Algorithm

The last lecture presented the crucial property:
$$
\begin{equation}
	\Delta (a) = \mu^{*} (a) - \mu(a) \precsim \sqrt{\frac{\log (T)}{n_{T}(a)}} \tag{1}
\end{equation}
$$
for any sub-optimal arm $a$.

##### 4.1 Instance-dependent and Instance-independet Bounds

**INSTANCE-DEPENDENT:** for the problem instance-dependent bound, we build off equation 1 and rearrange terms to get an upper-bound for $n_{T}(a)$:
$$
\begin{equation}
	n_{T}(a) \precsim \frac{\log (T)}{(\Delta (a))^{2}} \tag{4}
\end{equation}
$$

**INSTANCE-INDEPENDENT:** 
$$
\begin{equation}
	R (T) \precsim \sqrt{KT \log (T)} \tag{5}
\end{equation}
$$

##### 4.2 The UCB1 Algorithm

UCB1 Algorithm: Optimism in the face of Uncertainty.

![ucb1_algo](img/ucb1.png)

##### 4.3 Phased Successive Elimination

Phased successive elimination is a variation of successive elimination, notably producing an upper-bound that contains a log term that is a function of $K$, rather than $T$. The upper bound of pseudo-regret of this algorithm is $\sqrt{KT \log K}$.

![phased_successive_elimination](img/phased_successive_elimination.png)

### Lecture 05: Minimax Lower Bound for Finite-Arm Bandit Algorithms

**Definition 1 (Kullback-Leibler Divergence)** For two probability measures $\mathbb{P}$ and $\mathbb{Q}$ on the same probability space, the KL divergence is defined as:
$$
	D_{KL}(\mathbb{P}||\mathbb{Q}) = 
	\begin{cases} \mathbb{E}_{\mathbb{P}}\left[\log \frac{d\mathbb{P}}{d\mathbb{Q}}\right], \qquad \text{if } \mathbb{P} << \mathbb{Q}\\
	\infty, \qquad \qquad \qquad \text{otherwise}
	\end{cases}
$$
where $\frac{d \mathbb{P}}{d \mathbb{Q}}$ is the likelihood ratio and $\mathbb{P}<< \mathbb{Q}$ means that $\mathbb{P}$ is absolutely continuous w.r.t. $\mathbb{Q}$, which is true if for any set $A$ we have $\mathbb{Q}(A) = 0 \implies \mathbb{P}(A) = 0$.

When the probability measures $\mathbb{P}$ and $\mathbb{Q}$ have associated density functions, given by $p (x)$ and $q (x)$ respectively, then $\frac{d \mathbb{P}}{d \mathbb{Q}} (x) = \frac{p (x)}{q (x)}$, and we can write the KL divergence as $\int p (x)\log \frac{p (x)}{q (x)}dx$.


**Lemma 3 (Divergence Decomposition Lemma)** Let $\nu = (p_{1}, p_{2}, \dots, p_{k})$ be one instance of rewards distributions for a bandit scenario, and $\nu^{\prime} = (p_{1}^{\prime}, p_{2}^{\prime}, \dots, p_{k}^{\prime})$ be another. Fix an arbitrary policy $\pi$ consisting of the time-dependent policies $\pi_{t} (a_{t}| a_{1},x_{1}, a_{2}, x_{2},\dots, a_{t-1},x_{t-1})$ for $1 \leq t \leq T$. Let $P_{\nu}$ be the joint measure of $(A_{1}, X_{1}, A_{2}, \dots, A_{T}, X_{T})$ under instance $\nu$ and policy $\pi$, and $P_{\nu^{\prime}}$ be defined similarly for instance $\nu^{\prime}$ and policy $\pi$. Then the KL divergence between $P_{\nu}$ and $P_{\nu^{\prime}}$ can be written as:
$$
\begin{equation*}
	D (P_{\nu}|| P_{\nu^{\prime}}) = \sum_{i=1}^{k}\mathbb{E}_{\nu}[n_{T}(i)]D (p_{i}||p_{i}^{\prime}) \tag{2}
\end{equation*}
$$
where $n_{T}(i)$ is the number of times arm $i$ was pulled by time $T$. Note that $n_{T}(i)$ is a random variable depending on both the randomness of the environment and the policy.

One interpretation of this result is that given a particular KL divergence $D (P_{\nu}|| P_{\nu^{\prime}})$ for an algorithm, if $D (p_{i}||p_{i}^{\prime})$ is small, you expect to have to pull arm $i$ many times to figure out which instance you are in, while if $D (p_{i}||p_{i}^{\prime})$ is large, a good algorithm should be able to make the distinction with only a few pulls. Thus, the metric of $D (P_{\nu}|| P_{\nu^{\prime}})$ is important for understanding how well an algorithm behaves.

**Theorem 4.** For $T \geq K -1$ and $\nu$ from the family of Gaussian bandit instances,
$$
\begin{equation*}
	\inf_{\pi} \sup_{\nu} \mathbb{E}[R (T)] \succsim \sqrt{KT}
\end{equation*}
$$

### Lecture 06: Minimax Lower Bound and Thompson Sampling

##### 6.1 Minimax Lower Bound for Finite-Arm Bandits

**Definition 2 (Total Variation Distance)** Let $P$ and $Q$be two probability measures defined on $(\Omega, F)$, with density functions $p$ and $q$ respectively. The total variation distance (TV) between $P$ and $Q$ is defined
$$
\begin{equation*}
	TV (P,Q) = \sup_{A \in F} \left(P (A)- P (Q)\right) = \sup_{A \in F} \int_{x \in A} (p (x)- q (x))dx \tag{2}
\end{equation*}
$$
Clearly, for any $P$ and $Q$, $TV (P,Q) \in [0,1]$.

**Lemma 3 (Pinsker's Inequality)** Let $P$ and $Q$ be two probability measures. Then
$$
\begin{equation*}
	TV (P,Q) \leq \sqrt{ \frac{1}{2} D_{KL}(P || Q)} \tag{3}
\end{equation*}
$$

As TV-distance is always bounded by $1$, Pinsker's inequality becomes meaningless for very large $D_{KL}$. The following inequality on the other hand provides a non-trivial upper bound for TV-distance when $D_{KL}$ is large.

**Lemma 4.** Let $P$ and $Q$ be two probability measures. Then 
$$
\begin{equation*}
	1 - TV (P,Q) \geq \frac{1}{2} e^{-D_{KL}(P || Q)} \tag{4}
\end{equation*}
$$

##### 6.2 Thompson Sampling

Here we'll use Bayesian statistics to derive a simple algorithm for finite-arm bandits. Bayesian statistics is a method of statistical inference in which prior beliefs about the probability of a hypothesis are combined with new data to provide updated estimates. This is done by expressing the hypothesis as a probability distribution, and updating this distribution as new data is collected. This approach uses Bayes' theorem:
$$
\begin{align*}
	P(H|D) &= \frac{P(D|H)P(H)}{P(D)} \tag{5}\\
\end{align*}
$$
where $P (H|D)$ is the posterior probability of the hypothesis $H$ given the data $D$, $P (D|H)$ is the likelihood of the data given the hypothesis, $P (H)$ is the prior probability of the hypothesis and $P (D)$ is the probability of the data.

For example, suppose that we have rewards that comes from a Bernoulli distribution (the data), i.e. $x_{i} \sim \text{Bern}(r)$, for some $r \in [0,1]$ ($x_{i} \in \left\{0,1 \right\}$). We don't know the value r (the hypothesis), and we need a prior to find a posterior 

A conjugate prior is a prior distribution that belongs to the same family as the likelihood function. For example, if data $x_{i}$ is coming from a Bernoulli distribution, i.e. $x_{i} \sim \text{Bern}(r)$, for some $r \in [0,1]$ ($x_{i} \in \left\{0,1 \right\}$),

![thompson_sampling](img/algo_TS.png)
