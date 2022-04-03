from Crypto.PublicKey import RSA
from file_manager import key_to_file, file_to_key
import base64

for i in range(5):
    new_keyPair = RSA.generate(1024)
    key_to_file(new_keyPair,"client_key_%s"%(i))

#arr = []
#for i in range(5):
#    arr.append(file_to_key("doctor_key_%s"%(i)))

#print(arr)
#print(type(arr[0]))

