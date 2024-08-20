**Example 1** Consider a Cournot model where two firms, 1 and 2, produce a homogeneous good and compete in quantities. The inverse market demand is given by $p = 1 - Q$, where $Q$ is the sum of quantities produced by each firm. Unit costs of both firms are constant. Howerver, the unit cost may be either high, $c_{h}$, or low, $c_{l}$. We assume that $4 - 5 c_{h} + c_{l} \geq 0$. The joint probability distribution is given by 

$$
\begin{equation}
    F(c_{h}, c_{h}) = F(c_{h},c_{l}) = F(c_{l},c_{h}) = F(c_{l},c_{l}) = \frac{1}{4}.
\end{equation}
$$

---
a. Compute the symmetric Bayesian Nash equilibrium.

For each $i \in \left\{1,2\right\}$, $X_{i} = \left\{c_{h},  c_{l}  \right\}$. The profit function for each firm is given by:

$$
\begin{equation}
    \pi_{i}(q_{i}, q_{-i}, c_{i}) = \left(1 - q_{i} - q_{-i} \right)q_{i} - c_{i}q_{i}.
\end{equation}
$$

A Bayesian Nash Equilibrium are the decision functions $s_{1}^{*}(\cdot)$ and $s_{2}^{*}(\cdot)$, such that $\forall i \in \left\{1,2 \right\}$ , $\forall x_{i} \in X_{i}$ and $\forall s_{i} \in S_{i}$: 

$$
\begin{equation*}
	\int_{x_{-i} \in X_{-i}} \pi_{i}(s^{*}_{i}, s^{*}_{-i}, x_{i},x_{-i})d\hat{F}_{i}(x_{-i}|x_{i}) \geq \int_{x_{-i} \in X_{-i}} \pi_{i}(s_{i}, s^{*}_{-i}, x_{i},x_{-i})d\hat{F}_{i}(x_{-i}|x_{i})
\end{equation*}
$$
