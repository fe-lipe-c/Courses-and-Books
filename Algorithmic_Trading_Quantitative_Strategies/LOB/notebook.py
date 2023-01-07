"""Notebook to LOB application."""

from time import time_ns


start = time_ns()
start
end = time_ns()

total = end - start

total / 3600
nano_seconds_list = []

for i in range(10):
    nano_seconds_list.append(time_ns())

for i in range(10):
    print(nano_seconds_list[i] - nano_seconds_list[i - 1])
