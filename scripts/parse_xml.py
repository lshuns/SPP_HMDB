# -*- coding: utf-8 -*-
# @Author: lshuns
# @Date:   2021-06-27 16:55:02
# @Last Modified by:   lshuns
# @Last Modified time: 2021-07-18 22:27:52

# parse metabolites xml file
# Key facts:
###     1. the root for each element is metabolite
###     2. element under metabolite is unique
###     3. sub-element under element can be multiple
###     4. sub-element is last integrated node
###     5. HMDB_ID is under tag accession

import sys

from lxml import etree

import numpy as np
import pandas as pd

# ubiquitous prefix
U_PREFIX = '{http://www.hmdb.ca}'
N_U_PREFIX = 20

# def recurseChild_tag(node, parent_tag=None, tag_list=[]):
#     """
#     recursively get all the children tags
#     """

#     for i_child, child in enumerate(node):
#         child_tag = child.tag[N_U_PREFIX:]

#         # inherit parent name
#         if parent_tag is None:
#             tag_used = child_tag
#         else:
#             tag_used = parent_tag + '/' + child_tag
#             # remove saved parent name 
#             if i_child == 0:
#                 del tag_list[-1]
#         tag_list.append(tag_used)

#         # recurese
#         recurseChild_tag(child, parent_tag=tag_used, tag_list=tag_list)

# def recurseChild_bottom(node, inherit_list, desired_node_list=[]):
#     """
#     recursively find the bottom child with given inherit
#     """

#     # find the bottom child
#     tmp_node = metabolite
#     desired_node = []
#     for inherit in inherit_list:
#         tmp_node_list = tmp_node.findall(U_PREFIX+inherit)

#         for tmp_node_tmp in tmp_node_list:
#             tmp_node_tmp_list = tmp_node_tmp.findall(U_PREFIX+inherit)


#     for child_col in inherit_list:

#         if node is None:
#             print(f'Warning: {child_col} not found in recurseChild_bottom!')
#             return node

#         tmp_node = node.find(U_PREFIX+child_col)

#         # remove current layer
#         del inherit_list[0]

#         # recurese
#         tmp_node = recurseChild_bottom(tmp_node, inherit_list)

#     return tmp_node

def getAllTags(xml_file):
    """
    get all supported columns
        by looping over 5 metabolite
    """

    print('All supported tags:')

    MAX_metabolite = 5 
    tags_list = []
    i_metabolite = 0
    for _, metabolite in etree.iterparse(xml_file, tag=U_PREFIX+'metabolite'):

        for node in metabolite:
            N_child = len(node)
            if N_child == 0:
                tags_list.append([node.tag[N_U_PREFIX:]])
            else:
                for sub_node in node:
                    tags_list.append([node.tag[N_U_PREFIX:] + '/' + sub_node.tag[N_U_PREFIX:]])

        # iterate
        i_metabolite += 1
        if i_metabolite > MAX_metabolite:
            break

    # select unique names
    printed_tags = []
    for tags in tags_list:
        for tag in tags:
            if not tag in printed_tags:
                print(tag)
                print('\n')
                printed_tags.append(tag)

def parse_fromHMDB(xml_file, HMDB_ID_list, desired_cols): 
    """
    Extract info from xml file using HMDB ID
    """

    # total required elements
    N_tot = len(HMDB_ID_list)

    results_df = pd.DataFrame({'HMDB_ID': HMDB_ID_list})
    ## a flag for success of the first one
    flag0 = False
    for _, metabolite in etree.iterparse(xml_file, tag=U_PREFIX + 'metabolite'):
        # search with HMDB_ID
        HMDB_ID = metabolite.findtext(U_PREFIX + 'accession')

        if HMDB_ID in HMDB_ID_list:
            flag0 = True

            # loop over all desired columns
            for desired_col in desired_cols:

                # HMDB_ID is already saved
                if desired_col == 'HMDB_ID':
                    continue

                # see if contain children
                if '/' in desired_col:
                    parent_name, child_name = desired_col.split('/')

                    # get the parent node
                    parent_node = metabolite.find(U_PREFIX+parent_name)

                    # find children
                    desired_nodes = parent_node.findall(U_PREFIX+child_name)

                else:
                    desired_nodes = metabolite.findall(U_PREFIX+desired_col)
                
                # without this column
                if not desired_nodes:
                    print(f'Warning: {desired_col} is not in {HMDB_ID}!')
                    print(f'>>>>>>> will save with none')
                    results_df.loc[results_df['HMDB_ID']==HMDB_ID, f'{desired_col}_1'] = 'none'
                    continue

                else:
                    for i_node, desired_node in enumerate(desired_nodes):
                        # check if contain sub-node
                        N_node = len(desired_node)
                        if len(desired_node) > 0:
                            for subnode in desired_node:
                                subnode_tag = subnode.tag[N_U_PREFIX:]
                                subnode_val = subnode.text
                                results_df.loc[results_df['HMDB_ID']==HMDB_ID, f'{desired_col}_{i_node+1}/{subnode_tag}'] = subnode_val
                        else:
                            results_df.loc[results_df['HMDB_ID']==HMDB_ID, f'{desired_col}_{i_node+1}'] = desired_node.text
    
        # break out if all filled
        if flag0 and (not results_df.isnull().values.any()):
            break

    return results_df      

def Others2HMDB(xml_file, col_name, ID_list):
    """
    get the HMDB ID from other column info
    """

    # total required elements
    N_tot = len(ID_list)

    # lower letters for consistency
    ID_list = [ID.lower() for ID in ID_list]

    # df for results
    results_df = pd.DataFrame(columns=[col_name, 'HMDB_ID'])
    results_df[col_name] = ID_list

    for _, metabolite in etree.iterparse(xml_file, tag=U_PREFIX + 'metabolite'):

        # see if contain children
        if '/' in col_name:
            parent_name, child_name = col_name.split('/')

            # get the parent node
            parent_node = metabolite.find(U_PREFIX+parent_name)

            # find children
            desired_nodes = parent_node.findall(U_PREFIX+child_name)

        else:
            desired_nodes = metabolite.findall(U_PREFIX+col_name)

        if not desired_nodes:
            raise Exception(f'Cannot find {col_name}!')

        # search with given ID
        for desired_node in desired_nodes:
            given_ID = desired_node.text
            if given_ID.lower() in ID_list:
                # get the HMDB_ID
                HMDB_ID = metabolite.findtext(U_PREFIX + 'accession')
                results_df.loc[results_df[col_name]==given_ID.lower(), 'HMDB_ID'] = HMDB_ID
                break

        # break out if all filled
        if not results_df.isnull().values.any():
            break

    return results_df      
