#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:35:07 2020

@author: lshuns

Module to extract info from the original xml-form data, 
    then store into a panadas DataFrame.
"""

import xml.etree.ElementTree as et
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