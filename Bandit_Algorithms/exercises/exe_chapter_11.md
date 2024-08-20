### Chapter 11 - Exercises

---

```11.1``` (**Sampling from a Multinomial** ) In order to implment Exp3, you need a way to sample from the exponential weifhts distribution. Many programming languages provide a standard way to do this. For example, in Python you can use the Numpy library and ```numpy.random.multinomial```. In more basic languages, however, you only have access to a function ```rand()``` that returns a floating point number 'uniformly' distributed in $[0,1]$. Describe an algorithm that takes as input a probability vector $p \in \mathcal{P}_{k-1}$ and uses a single call to ```rand()``` to return $X \in [k]$ with $\mathbb{P}\left(X=i\right) = p _{i}$.  

```solution```

```python
def pseudo_multinomial(p):
    i = random.random()
    for j in range(len(p)):
        if i < sum(p[:j]) + p[j]:
            return j

def pseudo_multinomial_test(p, n):
    c = [0] * len(p)
    for i in range(n):
        c[pseudo_multinomial(p)] += 1

    return c


n = 100000
p = [0.1, 0.2, 0.5, 0.2]

result = pseudo_multinomial_test(p, n)
result = [round(x / n,2) for x in result]

result
>>Out[42]: ✓ Done
>>[0.1, 0.2, 0.5, 0.2]
```

---

```11.2``` (**Linear Regret for Deterministic Policies**) Show that for any deterministic policy $\pi$ there exists an environment $x \in [0,1]^{n \times k}$ such that $R_{n} (\pi, x) \geq n\left(1-\frac{1}{k}\right)$. What does your result say about the policies designed in Part II?

```solution```

The regret is defined as the difference between the reward of the best action in hindsight and the reward obtained by the policy $\pi$ over $n$ rounds: $R_{n} (\pi, x) = \max_{i \in [k]} \sum_{t=1}^{n} x_{t,i} - \sum_{t=1}^{n} x_{t, A_{t}}$

To prove the statement, we need to construct an environment such that the regret for policy $\pi$ is at least $n\left(1-\frac{1}{k}\right)$.

Let's construct an adversarial environment where for each round $t$, the reward for the action chosen by $\pi$ is $0$, and the reward for all other actions is $1$. This means that for each $t$, the reward vector $x_{t} = (x_{t,1}, x_{t,2}, \dots, x_{t,k})$ is such that $x _{t, A_{t}} = 0$ and $x_{t,i} = 1$ for all $i \neq A_{t}$

Since all actions except the one chosen by $\pi$ give a reward of $1$ at each time step, the best action in hindsight would have a total reward of $n$. The total reward obtained by policy $\pi$ over $n$ rounds is $0$. Therefore, the regret $R_{n}(\pi, x) = n-0=n$.

---

```11.3``` (**Maximum and Expections**) Show that the first inequality in (11.2) holds: Moving the maximum inside the expectation increases the value of the expectation.

```solution```
