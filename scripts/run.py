# -*- coding: utf-8 -*-
# @Author: lshuns
# @Date:   2021-06-27 18:54:41
# @Last Modified by:   lshuns
# @Last Modified time: 2021-07-18 22:10:54

import os
import sys
import argparse

import numpy as np
import pandas as pd

from parse_xml import getAllTags, parse_fromHMDB, Others2HMDB

__version__ = "SPP_HMDB v0.3"

# ++++++++++++++ parser for command-line interfaces
parser = argparse.ArgumentParser(
    description=f"{__version__}: extract chemical info from HMDB database.",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "--getAllTags", action="store_true",
    help="Get all supported tag names.\n")
parser.add_argument(
    "--input_info", type=str, metavar='param_file',
    help="A configuration file including input info.\n")
parser.add_argument(
    "--desired_info", type=str, metavar='param_file',
    help="A configuration file including desired info.\n")
parser.add_argument(
    '--data_base', type=str,  metavar='param_file', default='../data/hmdb_metabolites.xml',
    help="The HMDB database.\n")
parser.add_argument(
    '--version', action='version', version=__version__,
    help="The pipeline version.")

## arg parser
args = parser.parse_args()
input_file = args.input_info
desired_file = args.desired_info
xml_file = args.data_base

# get supported tag names
if args.getAllTags:
    getAllTags(xml_file)
    sys.exit()

# read input info
input_info = np.genfromtxt(input_file, dtype='str')
# check the name of the tags
if ':' in input_info[0]:
    tag_name = input_info[0].replace(":", "")
    print(f"Search info using `{tag_name}` as input...")
# tags
# print("Targets:")
tags = []
for tag in input_info[1:]:
    tags.append(tag)
# print(tags)
print('total number of tags', len(tags))

# read output info
out_info = np.genfromtxt(desired_file, dtype='str')
# check the output file name
if ':' in out_info[0]:
    outfile = out_info[0].replace(":", "")
# desired info
print("Desired info:")
res_names = []
for name in out_info[1:]:
    res_names.append(name)
print(res_names)

# search with HMDB ID
if tag_name == 'HMDB_ID':

    HMDB_ID_list = tags
    results_df = parse_fromHMDB(xml_file, HMDB_ID_list, res_names)

# search with other ID
else:

    # get the HMDB ID
    tmp_df = Others2HMDB(xml_file, tag_name, tags)
    HMDB_ID_list = tmp_df['HMDB_ID'].tolist()

    # search with HMDB ID
    results_df = parse_fromHMDB(xml_file, HMDB_ID_list, res_names)

    # get searching tags
    results_df = tmp_df.merge(results_df, on='HMDB_ID')

# save results to csv
if not os.path.exists('../results/'):
    os.makedirs('../results/')
out_path = '../results/' + outfile
results_df.to_csv(out_path, index=False)
print("Required info saved as csv in", out_path)