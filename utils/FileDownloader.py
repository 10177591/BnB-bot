import logging
from logging import config
import paramiko
import os
from read_config import *



class FileDownloader(object):
    ip = None
    port = None
    user = None
    password = None
    local_file_path = None
    remote_file_path = None
    abs_file_list = []
    ssh = None
    logger = None


    def __init__(self, config):
        logging.config.fileConfig('../config/logging.conf')
        self.logger = logging.getLogger('fileLogger')
        self.ip = config.get_serverip()
        self.port = config.get_serverport()
        self.user = config.get_username()
        self.password = config.get_password()
        self.remote_file_path = config.get_srcdir()
        self.local_file_path = config.get_dstdir()

    def download(self):
        sftp = self.ssh.open_sftp()
        self.list_remote_file(self.remote_file_path)
        for remote_file in self.abs_file_list:
            sub_path_name = remote_file[remote_file.index(self.remote_file_path) + len(self.remote_file_path):]
            local_file = self.local_file_path + sub_path_name
            dir_name = os.path.dirname(local_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            sftp.get(remote_file, local_file)
            self.logger.info('Download ' + remote_file + ' successfully.')

    def list_remote_file(self, remote_folder):
        sftp = self.ssh.open_sftp()
        file_list = sftp.listdir(remote_folder)
        for file in file_list:
            cmd = 'file ' + remote_folder + '/' + file + '|grep directory|wc -l'
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            res = stdout.readline().strip()
            if res == "1":
                self.list_remote_file(remote_folder + '/' + file)
            else:
                self.abs_file_list.append(remote_folder + '/' + file)



    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, int(self.port), self.user, self.password)
        self.logger.info('Connect to ' + self.ip + ' successfully.')

    def close(self):
        self.ssh.close()
        self.logger.info('Disconnect to ' + self.ip + ' successfully.')

if __name__ == '__main__':
    config = ConfigLoader().load_config('../config/product_config.json')
    downloader = FileDownloader(config)
    downloader.connect()
    downloader.download()
    downloader.close()

