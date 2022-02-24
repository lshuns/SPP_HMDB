#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:24:43 2020

@author: lshuns

Scripts to transfer xml-form info to feather-form info
"""

import re

import xml.etree.ElementTree as et
from lxml import etree

import numpy as np
import pandas as pd

def parse_XML_main(xml_file): 
    """
    Only extract the text from the main tags of the nodes
        (ignore all the sub-tag info)
    
    cols (or tags) are using the first element's tags
    """

    tree = et.parse(xml_file)
    root = tree.getroot()    
    
    # Use the first element's tags 
    #   as the reference
    cols = []
    cols_name = []
    for child in root[0]:
        cols.append(child.tag)
        cols_name.append(child.tag[20:])
    # print(cols)
    
    rows = []
    for node in root:
        vals = []
        for col in cols:
            if node.find(col) is not None:
                val = node.find(col).text
                if val != None:
                    if ('\n' in val):
                        val = 'TBD'
                vals.append(val)
            else:
                vals.append(None)
        rows.append({cols_name[i]: vals[i]
                        for i in range(len(cols))})
    
    df = pd.DataFrame(data=rows)
    df.rename(columns={'accession': 'HMDB_ID'}, inplace=True)

    return df      

def parse_XML_synonyms(xml_file): 
    """
    Extract synonyms for all the elements.
        for searching using synonyms.
    """

    rows = []
    for _, element in etree.iterparse(xml_file, tag='{http://www.hmdb.ca}synonyms'):
        if element.getparent().tag == '{http://www.hmdb.ca}metabolite':
            metabolite = element.getparent()

            # HMDB_ID
            HMDB_ID = metabolite.findtext('{http://www.hmdb.ca}accession')
            cols = ['HMDB_ID']
            vals = [HMDB_ID]

            # synonyms
            synonyms_node = metabolite.find('{http://www.hmdb.ca}synonyms')
            for i_syn in range(len(synonyms_node)):
                cols.append(f'synonym_{i_syn+1}')
                vals.append(synonyms_node[i_syn].text.lower())

            rows.append({cols[i]: vals[i]
                        for i in range(len(cols))})
    
    df = pd.DataFrame(data=rows)
    
    return df      

def parse_XML_taxonomy(xml_file): 
    """
    Extract sub-classes from taxonomy.
    """

    rows = []
    for _, element in etree.iterparse(xml_file, tag='{http://www.hmdb.ca}taxonomy'):

        ## get unique id
        metabolite = element.getparent()
        HMDB_ID = metabolite.findtext('{http://www.hmdb.ca}accession')
        cols_name = ['HMDB_ID']
        cols_val = [HMDB_ID]

        ## get child info
        for child in element:
            tag_full = child.tag
            tag_useful = re.search('{http://www.hmdb.ca}(.*)', tag_full).group(1)
            cols_name.append(f'taxonomy_{tag_useful}')
            cols_val.append(child.text)

        rows.append({cols_name[i]: cols_val[i]
                        for i in range(len(cols_val))})
        
    df = pd.DataFrame(data=rows)
    
    return df      


if __name__ == "__main__":
    import time
  
    # # ++++++++++++++++++++++++++ main data
    ############## 114222 unique rows
    # # original data
    # inpath = "../data/hmdb_metabolites.xml"
    # # out data
    # outpath = "../data/hmdb_metabolites_main.feather"
    # # Running
    # Start = time.time()
    # # main tags' info
    # # parse_XML_main(inpath)
    # df_main = parse_XML_main(inpath)
    # df_main.to_feather(outpath)
    # print("main tags' info saved in", outpath)
    # print("Finished in", time.time()-Start)
    # # Finished in 308.7

    # # ++++++++++++++++++++++++++ synonyms info
    # # original data
    # inpath = "../data/hmdb_metabolites.xml"
    # # out data
    # outpath = "../data/hmdb_metabolites_synonyms.feather"
    # # Running
    # Start = time.time()
    # # tags' info
    # df_syn = parse_XML_synonyms(inpath)
    # print(df_syn)
    # df_syn.to_feather(outpath)
    # print("Synonyms info saved in", outpath)
    # print("Finished in", time.time()-Start)
    # # Finished in 208.3602416515350

    # ++++++++++++++++++++++++++ taxonomy sub-classes
    # original data
    inpath = "../data/hmdb_metabolites.xml"
    # out data
    outpath = "../data/hmdb_metabolites_taxonomy.feather"
    # Running
    Start = time.time()
    # tags' info
    df_syn = parse_XML_taxonomy(inpath)
    # print(df_syn)
    df_syn.to_feather(outpath)
    print("taxonomy info saved in", outpath)
    print("Finished in", time.time()-Start)
    # Finished in 125.56326818466187

