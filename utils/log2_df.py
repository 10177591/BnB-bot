#
#
# Nokia Copyright...
############################################################

import pandas as pd
import re
import os.path
from glob import glob
from tensorflow.python.platform import gfile

class DFCreator():
    def get_file_list(self, log_dir):
        extensions = ['log','LOG']
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
            if dir_name == log_dir:
               continue
            #print("Looking for logs in '" + dir_name + "'")
            for extension in extensions:
                file_glob = os.path.join(log_dir, dir_name, '*.' + extension + "*")
                file_list.extend(gfile.Glob(file_glob))
            if not file_list:
                print('No files found')
                continue
            case_list[dir_name] = {
                'list' : file_list
                }
        return case_list

    def log2_dataframe(self, case_list, process_list):
        proc_count = len(case_list.keys())
        if proc_count == 0:
            print ('No process log found at')
            return -1
        proc_list = process_list.split(',')
        log_df = pd.DataFrame(columns=proc_list)
        log_proc = pd.DataFrame(columns=['case'])
        count = 0
        for dir_name, file_lists in case_list.items():
            file_list = file_lists['list']
            for file in file_list:
                base = os.path.basename(file)
                proc_name = os.path.splitext(base)[0]
                name = re.search(r'(\w+)',proc_name)
                if name is not None:
                    proc = name.group(1)
                    if proc in proc_list:
                        #print proc
                        with open(file) as f:
                            each_log = ''
                            for each_line in f:
                                each_log = each_log + each_line
                            log_df.set_value(count, proc, each_log)
                            log_proc.loc[count] = [dir_name]
            count = count + 1
        log_df['case_id'] = log_proc.case
       # print ('Number of logs read into data frame: %d' %(len(log_proc.index)))
       # print ('The name of the data frame %s' %(log_df.shape,))
       # print log_df.columns
        log_df.set_index(['case_id'], inplace=True)
        return log_df
        #print ('Number of logs read into data frame: %d' %(len(log_df.index)))

#loader = ConfigLoader()
#config = loader.load_config('./config/product_config.json')
#df_creator = DFCreator()
#case_list = df_creator.get_file_list('../data/logs/')
#df_creator.log2_dataframe(case_list, config.get_processlist())
