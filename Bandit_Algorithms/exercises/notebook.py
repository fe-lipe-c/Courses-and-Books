import numpy as np
import random


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
result = [round(x / n, 2) for x in result]
result
