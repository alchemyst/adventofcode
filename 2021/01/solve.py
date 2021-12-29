import pandas as pd
from aoc import solution


def increases(series):
    return (series.diff() > 0).sum()


lines = pd.read_csv("input.txt", header=None, names=["depth"])
depth = lines["depth"]

solution(increases(depth))
solution(increases(depth.rolling(3).sum()))
