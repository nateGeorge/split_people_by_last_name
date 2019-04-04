"""
Takes last names csv file, loads it, and breaks up into groups by last name.
"""

import numpy as np
import pandas as pd

df = pd.read_csv('cumulative_percent_surnames.csv')

# number of pieces to split in to
split_in_to = 5

# get cumulative percent values to split on
splits = [i / split_in_to for i in range(1, split_in_to)]

split_dict = {}
for s in splits:
    idx = abs(df['Cumulative_percent'] - s).idxmin()
    split_dict[s] = df.iloc[idx]['Surname']

# these are where the splits in the groups should happen
print(split_dict)
