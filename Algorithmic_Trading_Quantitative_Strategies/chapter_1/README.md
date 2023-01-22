# Chapter 1 - Trading Fundamentals

### Intraday Volume Distribution

To do a proper analysis of the intraday volume distribution, first we need to exclude from the data the opening and closing auctions, since their nature are different from the rest of the day. Thus, we delete from the analysis the first and last row for each day, the rows that contains the final quantity and price of the auctions.

A caveat that needs to be pointed out is the possibility of an auction occurring over the normal trading time, when, for example, the analyzed asset exceeds a certain variation. In this situation, since the data is not annotated with this information, it will be part of the final analysis. Nevertheless, this kind of data in the normal intraday trading contributes to a greater differentiation between the distributions.

### To Do

- [ ] Intraday volume distribution
- [ ] KL divergence for volume distribution
- [ ] Figure 1.4: Futures Rolling

![figure1_4](img/futures_roll.png =600x)

- [ ] Distribution of spread size
- [ ] Disbribution of trade size
- [ ] X-day average auction volume
- [ ] Beta with respecto to an index or sector (plain beta or asymmetric up-days/down-days beta)
- [ ] correlation matrix
- [ ] VWAP
