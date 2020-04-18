#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:44:53 2020

@author: lshuns

Scripts to search desired info 
"""

import numpy as np
import pandas as pd

import os
import sys
# Self-defined package
sys.path.insert(0, os.path.realpath('..')) 
from source import io_related

# read input info
input_info = np.genfromtxt('../input_info.param', dtype='str')
# check the name of the tags
if ':' in input_info[0]:
    tag_name = input_info[0].replace(":", "")
    print("Search info using `{:}` as input...".format(tag_name))
# tags
print("Called tags:")
tags = []
for tag in input_info[1:]:
    tags.append(tag)
    print("     ", tag)

# read output info
out_info = np.genfromtxt('../desired_info.param', dtype='str')
# check the output file name
if ':' in out_info[0]:
    outfile = out_info[0].replace(":", "")
# desired info
print("Desired info:")
res_names = []
for name in out_info[1:]:
    res_names.append(name)
    print("     ", name)

# read database
df_main = pd.read_feather("../data/hmdb_metabolites_main.feather")

# search tags & values
df_main_selec = df_main[df_main[tag_name].isin(tags)][res_names]
# print(df_main_selec)

# save results to csv
out_path = '../results/' + outfile
io_related.save_df(df_main_selec, out_path, file_form='csv')
print("Required info saved as csv in", out_path)