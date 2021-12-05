#!/usr/bin/env python

import pandas as pd

def increases(series):
    return (series.diff() > 0).sum()

#%%
lines = pd.read_csv('input.txt', header=None, names=['depth'])
depth = lines['depth']

print('Increases:', increases(depth))
# %%
print('Windowed:', increases(depth.rolling(3).sum()))