# Fixed Income Applied to the Brazilian Market

## Chapter 1: Introduction

### 1.2 Returns and Interest Rates

Returns show the relative change in the price of an asset or the value of a portfolio over a period of time. They are usually expressed as a percentage and are useful for comparing investments. When dealing with fixed income instruments and loans, returns are called interest rates. There are two ways of expressing interest rates: discrete (also called simple or arithmetic) and continuous (also called logarithmic or geometric).

Let $t$ be the current date and $T > t$ be the horizon of an investment. The investment period is denoted by $\tau = T-t$. Let $V$ be the value of an investment, so that $V _{t}$ is the amount invested and $V _{T}$ is the redemption value. The discrete spot rate between $t$ and $T$ (denoted by $R _{t,T}$ or $R _{t}(\tau)$) is defined by:
$$
\begin{equation}
    R _{t,T} = R _{t}(\tau) = \left( \frac{V _{T}}{V _{t}}\right)^{1/\tau} - 1 \tag{1.1}
\end{equation}
$$
![image](/img/discrete_spot_rate.png =600x400)


and the continuous spot rate (denoted by $r _{t,T}$ or $r _{t}(\tau)$) is defined by:
$$
\begin{equation}
    r _{t,T} = r _{t}(\tau) = \frac{1}{\tau} \ln \frac{V _{T}}{V _{t}} \tag{1.2}
\end{equation}
$$
Note that both definitions of the interest rate dependent directly of the relative value change ($V _{T}/V _{t}$) and inversely of the investment period ($\tau$). These two properties provide an interesting intuition: a large valuation in a short period of time implies significant returns.

In Brazil, the convention most adopted by the financial market considers the year to have 252 working days. That is,
$$
\begin{equation*}
	\tau = \frac{\small\text{number of working days between $t$ and $T$}}{252}
\end{equation*}
$$
