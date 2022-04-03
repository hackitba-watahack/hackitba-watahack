import pickle
from Crypto.PublicKey import RSA
import base64

def var_to_file(my_var, file_name):
    with open(file_name,'wb') as file:
        pickle.dump(my_var,file)

def file_to_var(file_name):
    with open(file_name,'rb') as file:
        return pickle.load(file)

def key_to_file(my_key, file_name):
    data = base64.b64encode(my_key.export_key()).decode("utf-8")
    var_to_file(data, file_name)

def file_to_key(file_name):
    data = file_to_var(file_name)
    return RSA.import_key(base64.b64decode(data))
