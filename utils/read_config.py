#
#
# Nokia Copyright...
############################################################

import json

class Config (object):
    """
        Create a product configuration object from JSON.
        Support nested JSON Objects for each product. Currently only one
        is supported.

       Argument: JSON Object from the configuration file.
    """
    def __init__(self, attrs):
       self.product = attrs["product"]
       self.logtype = attrs["logtype"]
       self.server = attrs["server"]
       self.port = attrs["port"]
       self.username = attrs["username"]
       self.password = attrs["password"]
       self.srcdir = attrs["src_dir"]
       self.dstdir = attrs["dst_dir"]
       self.protocol = attrs["protocol"]

    def __str__(self):
        return "%s;%s" %(self.product, self.logtype)

    def login_info(self):
        return "%s:%s:%s" %(self.server, self.port, self.username)

    def get_product(self):
        return self.product

    def get_logtype(self):
        return self.logtype

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

class ConfigLoader (object):
    '''
        Create a confiuration loaded which can read JSON config files
    '''
    def load_config (self, attrs):
        with open (attrs) as data_file:
            config = json.load(data_file, object_hook=load_json)
        return config

def load_json (json_object):
    return Config (json_object)

loader = ConfigLoader()
config = loader.load_config('../config/product_config.json')

print config
