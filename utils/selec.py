# -*- coding: utf-8 -*-
# @Author: lshuns
# @Date:   2021-06-29 18:06:50
# @Last Modified by:   lshuns
# @Last Modified time: 2021-06-29 21:00:35

### select group of columns based on desired values

import pandas as pd 
import numpy as np

import re

# ++++++++++++++ I/O

# queried catalogue
inpath_query = '../results/test.csv'

outpath = '../results/test_Blood.csv'
# outpath = '../results/test_Feces.csv'

# ++++++++++++++ general setting

# group base name
col_base_name_list = ['normal_concentrations/concentration_', 'abnormal_concentrations/concentration_']

# saved columns
col_desired_name_list = [['biospecimen', 'concentration_value', 'concentration_units', 'subject_age'],
                         ['biospecimen', 'concentration_value', 'concentration_units', 'patient_age', 'patient_information']]

# selecting based column name
col_selec_name = 'biospecimen'

# desired value
desired_val = 'Blood'
# desired_val = 'Feces'

# +++++++++++++ workhorse

# load query catalogue
cata_query = pd.read_csv(inpath_query)
print('queried catalogue loaded from', inpath_query)

# # 1. get the max index for groups
# # 2. get the member name
# index_max_list = []
# # members_list = []
# for col_base_name in col_base_name_list:
#     # number of letters in base name
#     N_base = len(col_base_name)
#     # find the max index
#     index_max = 1
#     # members = []
#     for col in cata_query.columns:
#         # if certain column belong to the group
#         if col[:N_base] == col_base_name:
#             # 1. get the index 
#             index_tmp = int(re.findall(r'\d+', col)[0])
#             # compare to current max
#             if index_tmp > index_max:
#                 index_max = index_tmp
#             # # 2. get the member col
#             # member_tmp = col.split('/')[-1]
#             # if not member_tmp in members:
#             #     members.append(member_tmp)
#     index_max_list.append(index_max)
#     # members_list.append(members)
# print('max index', index_max_list)
# # print('all members', members_list)

# 1. get the max index for groups
# 2. remove not desired name
index_max_list = []
for i_col_base, col_base_name in enumerate(col_base_name_list):
    # number of letters in base name
    N_base = len(col_base_name)
    # members
    members = col_desired_name_list[i_col_base]
    # find the max index
    index_max = 1
    all_col = cata_query.columns
    for col in all_col:
        # if certain column belong to the group
        if col[:N_base] == col_base_name:
            # 1. get the index 
            index_tmp = int(re.findall(r'\d+', col)[0])
            # compare to current max
            if index_tmp > index_max:
                index_max = index_tmp
            # # 2. remove not desired name 
            member_tmp = col.split('/')[-1]
            if not member_tmp in members:
                cata_query.drop(columns=col, inplace=True)
    index_max_list.append(index_max)
print('max index', index_max_list)

# mask undesired columns
for i_col_base, col_base_name in enumerate(col_base_name_list):
    # number of letters in base name
    N_base = len(col_base_name)
    # max index
    index_max = index_max_list[i_col_base]
    # members
    members = col_desired_name_list[i_col_base]

    for index_tmp in range(index_max):
        # select based name
        col_selec_name_tmp = col_base_name + str(index_tmp + 1) + '/' + col_selec_name
        mask_undesired = cata_query[col_selec_name_tmp] != desired_val
        # those not saved marked as none
        for member in members:
            col_member_name_tmp = col_base_name + str(index_tmp + 1) + '/' + member
            cata_query.loc[mask_undesired, col_member_name_tmp] = np.NaN

# delete columns without any info for neat catalogue
N_all = len(cata_query)
all_col = cata_query.columns
for col in all_col:
    N_noinfo = np.sum(cata_query[col].isnull())
    if N_all == N_noinfo:
        cata_query.drop(columns=col, inplace=True)

# save
cata_query.to_csv(outpath, index=False)
print('selected catalogue saved to', outpath)
