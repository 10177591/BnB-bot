#
#
# Nokia Copyright...
############################################################

import pandas as pd
import numpy as np
import math
import re
from utils.log2_df import DFCreator
from utils.read_config import ConfigLoader

def feature_wcount(token, input_df):
    if token == 'wcount':
        count_df = input_df.applymap(wordcount)
    elif token == 'expcount':
        count_df = input_df.applymap(expcount)
    elif token == 'dbgcount':
        count_df = input_df.applymap(dbgcount)
    return count_df

def wordcount (log):
    matched = re.findall(r'(\w+)',log)
    return len(matched)

def expcount (log):
    matched = re.findall(r'exception|error|failure|warning',log, re.IGNORECASE)
    return len(matched)

def dbgcount (log):
    matched = re.findall(r'debug|info',log, re.IGNORECASE)
    return len(matched)

loader = ConfigLoader()
config = loader.load_config('./config/product_config.json')

df_creator = DFCreator()
case_list = df_creator.get_file_list('./data/logs/')

input_df = df_creator.log2_dataframe(case_list, config.get_processlist())

input_df[input_df.isnull()] = 'empty'

wcount_df = feature_wcount('wcount', input_df)
expcount_df = feature_wcount('expcount', input_df)
dbgcount_df = feature_wcount('dbgcount', input_df)
expcount_df = feature_wcount('expcount', input_df)
print wcount_df
print expcount_df
print dbgcount_df
