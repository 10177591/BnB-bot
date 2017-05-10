#
#
# Nokia Copyright...
############################################################

import json

class Config():
    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj

    def __str__(self):
        return "%s;%s" %(self.product, self.logtype)

    def login_info(self):
        return "%s:%s:%s" %(self.server, self.port, self.username)

    def get_product(self):
         return self.product

    def get_serverip(self):
        return self.server

    def get_serverport(self):
        return self.port
    
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_srcdir(self):
        return self.srcdir

    def get_dstdir(self):
        return self.dstdir

    def get_protocol(self):
        return self.protocol

    def get_logtype(self):
        return self.read_logs.log_type

    def get_readlogs(self):
        return self.readlogs
    
    def get_logurl(self):
        return self.read_logs.log_url
    
class ConfigLoader (object):
    '''
        Create a confiuration loaded which can read JSON config files
    '''
    def load_config (self, attrs):
        with open (attrs) as data_file:
            config = json.load(data_file, object_hook=Config.from_dict)
        return config

loader = ConfigLoader()
config = loader.load_config('../config/product_config.json')

#print config.get_logurl()
#print config.get_serverport()
