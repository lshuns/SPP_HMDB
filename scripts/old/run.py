#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:44:53 2020

@author: lshuns

Scripts to search desired info 
"""

import os
import argparse

import numpy as np
import pandas as pd

__version__ = "SPP_HMDB v0.2"

# ++++++++++++++ parser for command-line interfaces
parser = argparse.ArgumentParser(
    description=f"{__version__}: extract chemical info from HMDB database.",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "--input_info", type=str, metavar='param_file',
    help="A configuration file including input info.\n")
parser.add_argument(
    "--desired_info", type=str, metavar='param_file',
    help="A configuration file including desired info.\n")
parser.add_argument(
    '--version', action='version', version=__version__,
    help="The pipeline version.")

## arg parser
args = parser.parse_args()
input_file = args.input_info
desired_file = args.desired_info

# read input info
input_info = np.genfromtxt(input_file, dtype='str')
# check the name of the tags
if ':' in input_info[0]:
    tag_name = input_info[0].replace(":", "")
    print(f"Search info using `{tag_name}` as input...")
tag_name0 = tag_name
# tags
print("Targets:")
tags = []
for tag in input_info[1:]:
    tags.append(tag)
print(tags)

# read output info
out_info = np.genfromtxt(desired_file, dtype='str')
# check the output file name
if ':' in out_info[0]:
    outfile = out_info[0].replace(":", "")
# desired info
print("Desired info:")
res_names = [tag_name]
for name in out_info[1:]:
    res_names.append(name)
print(res_names)


# check if the input tag is synonym
if tag_name == 'synonyms':

    # transfer everything to lowercase for easy comparison
    tags = [x.lower() for x in tags]

    # read synonym info
    df = pd.read_feather("../data/hmdb_metabolites_synonyms.feather")
    tags_id = []
    tags_syn = []
    N_matched = 0 
    N_tot = len(tags)
    print('Total number of tags', N_tot)
    for col in df:
        if col != 'HMDB_ID':
            mask_selected = df[col].isin(tags)
            N_matched_tmp = np.sum(mask_selected)
            if N_matched_tmp > 0:
                tags_id.extend(df.loc[mask_selected, 'HMDB_ID'].values.tolist())
                tags_syn.extend(df.loc[mask_selected, col].values.tolist())

                # number of tags matched
                N_matched += N_matched_tmp
                print(f'number matched in {col}: {N_matched_tmp}')

    # get the HMDB_ID 
    tags = tags_id
    tag_name = 'HMDB_ID'

    # build a dataframe for synonyms
    df_syn = pd.DataFrame({'HMDB_ID': tags_id, 'synonyms': tags_syn})
    # print(df_syn)

    # synonym is not in the main data file
    if 'HMDB_ID' not in res_names:
        res_names[0] = 'HMDB_ID'
    else:
        res_names = res_names[1:]

# read database
df = pd.read_feather("../data/hmdb_metabolites_main.feather")
# search tags & values
try:
    df_main_selec = df[df[tag_name].isin(tags)][res_names]
    # print(df_main_selec)
## include sub-classes
except KeyError:
    tmp_name_str = '_'.join(res_names)

    # +++++++++++ taxonomy
    if 'taxonomy' in tmp_name_str:
       df_sub = pd.read_feather("../data/hmdb_metabolites_taxonomy.feather")
       df = df.merge(df_sub, on='HMDB_ID', how='left')

    df_main_selec = df[df[tag_name].isin(tags)][res_names]   

 # add synonym to the output
if (tag_name0 == 'synonyms'):
    df_main_selec = df_main_selec.merge(df_syn, on='HMDB_ID')  

# save results to csv
if not os.path.exists('../results/'):
        os.makedirs('../results/')
out_path = '../results/' + outfile
df_main_selec.to_csv(out_path, index=False)
print("Required info saved as csv in", out_path)