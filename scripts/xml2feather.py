#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:24:43 2020

@author: lshuns

Scripts to transfer xml-form info to feather-form info
"""

import time

import pandas as pd
import numpy as np

import os
import sys
# Self-defined package
sys.path.insert(0, os.path.realpath('..')) 
from source import io_related, xml

# ++++++++++++++++++++++++++ Setting
# original data
inpath = "../data/hmdb_metabolites.xml"
# out data
outpath = "../data/hmdb_metabolites_main.feather"
# save form
save_form = 'feather'


# ++++++++++++++++++++++++++ Running
Start = time.time()
# main tags' info
df_main = xml.parse_XML_main(inpath)
io_related.save_df(df_main, outpath, file_form=save_form)
print("main tags' info saved in", outpath)
print("Finished in", time.time()-Start)