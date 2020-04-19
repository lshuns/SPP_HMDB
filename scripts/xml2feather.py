#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:24:43 2020

@author: lshuns

Scripts to transfer xml-form info to feather-form info
"""

import xml.etree.ElementTree as et

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
    for child in root[0]:
        cols.append(child.tag)
    print(cols)
    
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
        rows.append({cols[i]: vals[i]
                        for i in range(len(cols))})
    
    df = pd.DataFrame(data=rows)
    
    return df      

if __name__ == "__main__":
    import time
  
    # ++++++++++++++++++++++++++ Setting
    # original data
    inpath = "../data/hmdb_metabolites.xml"
    # out data
    outpath = "../data/hmdb_metabolites_main.feather"

    # ++++++++++++++++++++++++++ Running
    Start = time.time()
    # main tags' info
    df_main = parse_XML_main(inpath)
    df_main.to_feather(outpath)
    print("main tags' info saved in", outpath)
    print("Finished in", time.time()-Start)