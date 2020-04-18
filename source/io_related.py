#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:17:38 2020

@author: lshuns

Module with all input/output related functions 
"""

def save_df(out_df, out_path, file_form='csv'):
    """
    save the dataframe into certain forms
    """
    if file_form == 'csv':
        out_df.to_csv(out_path, index=False)
        # print("Dataframe saved as csv in", out_path)
    elif file_form =='feather':
        out_df.to_feather(out_path)
        print("Dataframe saved as feather in", out_path)
    else:
        raise Exception("Unsupported file form!")

