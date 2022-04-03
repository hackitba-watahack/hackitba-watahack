import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha512

debug = False

def encrypt(message, pubKey):
    encryptor = PKCS1_OAEP.new(pubKey)
    return encryptor.encrypt(str.encode(message))

def desencrypt(encmes, keyPair):
    decryptor = PKCS1_OAEP.new(keyPair)
    return decryptor.decrypt(encmes)

def sign(message, private_exp, modulus):
    if type(message) == str:
        message = str.encode(message)
    hash = int.from_bytes(sha512(message).digest(), byteorder='big')
    return pow(hash, private_exp, modulus)

def verify(message, signature, public_exp, modulus):
    if type(message) == str:
        message = str.encode(message)
    hash = int.from_bytes(sha512(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, public_exp, modulus)
    return hash == hashFromSignature

if debug:

    keyPair = RSA.generate(1024)
    pubKey = keyPair.public_key()

    msg = "Si tu lo deseas puedes volar"

    encrypted = encrypt(msg,pubKey)
    print(encrypted)
    decrypted = desencrypt(encrypted, keyPair)
    print(decrypted)
    signature = sign(encrypted, keyPair.d, keyPair.n)
    print(hex(signature))
    valid = verify(encrypted, signature, pubKey.e, pubKey.n)
    print(valid)
