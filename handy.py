from Crypto.PublicKey import RSA
from file_manager import key_to_file, file_to_key, var_to_file
import base64


# CREA KEYS Y LAS GUARDA
#for i in range(5):
#    new_keyPair = RSA.generate(1024)
#    key_to_file(new_keyPair,"client_key_%s"%(i))

# CARGA KEYS
arr = []
for i in range(5):
    arr.append(file_to_key("doctor_key_%s"%(i)))

#print(arr)
#print(type(arr[0]))

# CREA DATABASE DE DOCTORES

#doctor_database = []
#for i in range(5):
#    doctor_database.append((arr[i].e,arr[i].n))

#var_to_file(doctor_database, 'doctor_database')