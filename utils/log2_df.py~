#
#
# Nokia Copyright...
############################################################

import pandas as pd
import re
import os.path
from glob import glob
from tensorflow.python.platform import gfile

def get_file_list(log_dir):

    extensions = ['log','LOG']
    file_list = []
    if not gfile.Exists(log_dir):
        print("Log directory '" + log_dir + "' not found.")
        return None
    result = {}
    sub_dirs = [x[0] for x in gfile.Walk(log_dir)]
    # The root directory comes first, so skip it.
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir = False
            continue
        dir_name = os.path.basename(sub_dir)
        if dir_name == log_dir:
           continue
        #print("Looking for logs in '" + dir_name + "'")
        for extension in extensions:
            file_glob = os.path.join(log_dir, dir_name, '*.' + extension + "*")
            file_list.extend(gfile.Glob(file_glob))
        if not file_list:
            print('No files found')
            continue
    return file_list

def log2_dataframe(file_list):
    log_df = pd.DataFrame(columns=['log','procid'])
    count = 0
    for file in file_list:
        #print file
        with open (file) as f:
            each_log = ''
            log_dict = {}
            for each_line in f:
                each_log = each_log + each_line
            base = os.path.basename(file)
            procid = os.path.splitext(base)[0]
            log_df.loc[count] = [each_log, procid]
            count = count+1
    print ('Number of logs read into data frame: %d' %(len(log_df.index)))
    return log_df

file_list = get_file_list('../tmp')
log2_dataframe(file_list)
