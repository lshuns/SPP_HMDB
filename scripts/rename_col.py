#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:44:49 2020

@author: lshuns

Scripts to rename the column names
"""

import pandas as pd

import os
import sys
# Self-defined package
sys.path.insert(0, os.path.realpath('..')) 
from source import io_related

filename = "../data/hmdb_metabolites_main.feather"

# read database
df_main = pd.read_feather(filename)

# rename
df_main.rename(columns={'accession': 'HMDB_ID'}, inplace=True)
for col in df_main.columns:
    print(col)

# output
df_main.to_feather(filename)
print("Renamed data saved as feather in", filename)