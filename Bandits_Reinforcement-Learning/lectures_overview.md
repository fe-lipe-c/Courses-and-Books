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
