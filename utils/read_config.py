import json

json_string = '{"product" : "location" , "logtype" : "daily ta"}'

class Config (object):
    def __init__(self, attrs):
       self.product = attrs["product"]
       self.logtype = attrs["logtype"]
       self.datadir = attrs["data_dir"]
       self.server = attrs["server"]
       self.port = attrs["port"]
       self.username = attrs["username"]
       self.password = attrs["password"]

    def __str__(self):
        return "%s;%s" %(self.product, self.logtype)

    def login_info(self):
        return "%s:%s:%s" %(self.server, self.port, self.username)

def load_config(json_object):
    return Config (json_object)


with open ('../config/product_config.json') as data_file:
    config =  json.load(data_file, object_hook=load_config)
    print config.login_info()
