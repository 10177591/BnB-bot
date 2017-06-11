#
#
# Nokia Copyright...
############################################################
import pandas as pd
import re
import os.path
from glob import glob
from tensorflow.python.platform import gfile
from read_config import ConfigLoader

class DFCreator():
    def get_file_list(self, log_dir):
        extensions = ['log','LOG','nm']
        if not gfile.Exists(log_dir):
            print("Log directory '" + log_dir + "' not found.")
            return None
        case_list = {}
        sub_dirs = [x[0] for x in gfile.Walk(log_dir)]
        # The root directory comes first, so skip it.
        is_root_dir = True
        for sub_dir in sub_dirs:
            file_list = []
            if is_root_dir:
                is_root_dir = False
                continue
            dir_name = os.path.basename(sub_dir)
            log_dir = os.path.dirname(sub_dir)
            if dir_name == log_dir:
               continue
            #print("Looking for logs in '" + dir_name + "'")
            for extension in extensions:
                file_glob = os.path.join(log_dir, dir_name, '*' + extension + "*")
                file_list.extend(gfile.Glob(file_glob))
            if not file_list:
               # print('No files found')
                continue
            case_list[log_dir+dir_name] = {
                'list' : file_list
                }
        return case_list

    def log2_dataframe(self, case_list, process_list):
        proc_count = len(case_list)
        if proc_count == 0:
            print ('No process log found at')
            return -1
        proc_list = process_list.split(',')
        proc_list.insert(0,'date')
        proc_list.insert(1,'case')
        log_df = pd.DataFrame(columns=proc_list)
        log_proc = pd.DataFrame(columns=['case','date'])
        count = 0
        for dir_name, file_lists in case_list.items():
           # print dir_name
            file_list = file_lists['list']
            for file in file_list:
                base = os.path.basename(file)
                dirname =  os.path.dirname(file)
                base1 = re.search(r'(.*)\/(.*)\/(.*)', dirname).group(3)
                base2 = re.search(r'(.*)\/(.*)\/(.*)', dirname).group(2)
                #print base1 + "_" + base2
                proc_name = os.path.splitext(base)[0]
                name = re.search(r'(\w+)',proc_name)
                if name is not None:
                    proc = name.group(1)
                    if proc in proc_list:
                        with open(file) as f:
                            each_log = ''
                            for each_line in f:
                                each_log = each_log + each_line
                            log_df.set_value(count, proc, each_log)
            log_df.set_value(count, 'date', base2)
            log_df.set_value(count, 'case', base1)
            count = count + 1
       # print ('Number of logs read into data frame: %d' %(len(log_proc.index)))
       # print ('The size of the data frame %s' %(log_df.shape,))
       # print log_df.columns
        print log_df.loc[:, 'lppserver_LPP']
        log_df.set_index(['date','case'], inplace=True)
        return log_df
        #print ('Number of logs read into data frame: %d' %(len(log_df.index)))

loader = ConfigLoader()
config = loader.load_config('../config/product_config.json')
df_creator = DFCreator()
file_list = df_creator.get_file_list('../data/')
df_creator.log2_dataframe(file_list, config.get_processlist())
