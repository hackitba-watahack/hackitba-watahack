from drive import init_module,open_folder,create_file_from_local,get_list_from_folder,download_file,change_content_from_string, open_sub_folder, get_file_from_folder
from file_manager import var_to_file, file_to_var, key_to_file, file_to_key
from encrypting import generate_keyPair, encrypt, desencrypt, sign, verify
from enum import Enum

debug = True

class regType(Enum):
    REGULAR = 0
    NEW_DOC = 1

def is_doctor_on_database(public_exp, modulus):
    doctor_database = file_to_var('doctor_database')
    answer = False
    for item in doctor_database:
        if public_exp == item[0] and modulus == item[1]:
            answer = True
            break
    return answer

def encrypt_and_sign(message, private_key):
    public_key = private_key.public_key()
    encmes = encrypt(message, public_key)
    signature = sign(encmes, private_key.d, private_key.n)
    return (encmes, signature, public_key.e, public_key.n)

def make_new_register(message, doctor_private_key, client_private_key):
    doctor_enc = encrypt_and_sign(message, doctor_private_key)
    client_enc = encrypt_and_sign(message, client_private_key)
    return (regType.REGULAR, doctor_enc, client_enc)

def validate_register(register):
    doctor_enc = register[1]
    client_enc = register[2]

    if is_doctor_on_database(doctor_enc[2],doctor_enc[3]) and \
        verify(doctor_enc[0],doctor_enc[1],doctor_enc[2],doctor_enc[3]) and \
        verify(client_enc[0],client_enc[1],client_enc[2],client_enc[3]):
        return True
    else:
        return False

def get_related_blocks(key_is_doctor,public_key,block_chain):
    related_blocks = []
    for register in block_chain:
        if key_is_doctor:
            if register[1][2] == public_key.e and register[1][3] == public_key.n:
                related_blocks.append(register)
        else:
            if register[2][2] == public_key.e and register[2][3] == public_key.n:
                related_blocks.append(register)
    return related_blocks

def decrypt_related_common_blocks(doctor_private_key,client_public_key,block_chain): # incluye NEW_DOC
    related_to_client = get_related_blocks(False,client_public_key,block_chain)
    related_to_both = get_related_blocks(True,doctor_private_key.public_key(),related_to_client)
    decrypted = []
    for register in related_to_both:
        decrypted.append(desencrypt(register[1][0],doctor_private_key))
    return decrypted

def get_full_history(client_private_key,block_chain):
    history = get_related_blocks(False,client_private_key.public_key(),block_chain)
    decrypted = []
    for register in history:
        if register[0] == regType.REGULAR: # No incluimos NEW_DOC por redundancia
            decrypted.append(desencrypt(register[2][0],client_private_key))
    return decrypted

def make_new_history(client_private_key, doctor_private_key, block_chain):
    decrypted_history = get_full_history(client_private_key,block_chain)
    new_message = ""
    for message in decrypted_history:
        new_message += str(message)
        new_message += " - "
    doctor_enc = encrypt_and_sign(new_message, doctor_private_key)
    client_enc = encrypt_and_sign(new_message, client_private_key)
    return (regType.NEW_DOC,doctor_enc,client_enc)

#def is_register_on_block_chain(register,block_chain):
#    for reg in block_chain:
#        if reg == register:
#            return True
#    return False


if debug:
    print("debug")
    #   CREAR Y VALIDAR UN REGISTRO
    #message = "A la grande le puse cuca"
    #doc_key = file_to_key('doctor_key_0')
    #cli_key = file_to_key('client_key_0')
    #new_reg = make_new_register(message, doc_key, cli_key)
    #print(validate_register(new_reg))


    ##   CREAR UNA BLOCKCHAIN A PARTIR DE REGISTROS (siendo el hospital)
    drive = init_module()
    main_folder = open_folder(drive,"watahack_folder1")
    hospital_folder = open_sub_folder(drive, main_folder, "Node_1")
    
    my_block_chain = []

    my_block_chain.append(make_new_register("PRIMER REGISTRO",file_to_key("doctor_key_0"),file_to_key("client_key_0")))
    my_block_chain.append(make_new_register("SEGUNDO REGISTRO",file_to_key("doctor_key_0"),file_to_key("client_key_1")))
    my_block_chain.append(make_new_register("TERCER REGISTRO",file_to_key("doctor_key_1"),file_to_key("client_key_1")))
    my_block_chain.append(make_new_register("CUARTO REGISTRO",file_to_key("doctor_key_1"),file_to_key("client_key_3")))
    my_block_chain.append(make_new_register("QUINTO REGISTRO",file_to_key("doctor_key_0"),file_to_key("client_key_0")))

    ##new_thingy = make_new_register("PRIMER REGISTRO",file_to_key("doctor_key_0"),file_to_key("client_key_0"))
    
    #print(is_register_on_block_chain(new_thingy),my_block_chain)

    var_to_file(my_block_chain,"my_block_chain")
    create_file_from_local(drive,hospital_folder,"my_block_chain")

    ##   (siendo el medico) COPIANDO DATOS DEL HOSPITAL, PARA VER DATOS DE UN PACIENTE
    #drive = init_module()
    #main_folder = open_folder(drive,"watahack_folder1")
    #hospital_folder = open_sub_folder(drive, main_folder, "Node_1")
    #file = get_file_from_folder(drive,hospital_folder,"my_block_chain")
    #download_file(drive,file,"copied_block_chain")
    #block_chain =  file_to_var("copied_block_chain")
    #print(block_chain)

    #cli_key = file_to_key("client_key_1")
    #related_blocks = get_related_blocks(False,cli_key.public_key(),block_chain)
    #print(related_blocks)
    #doc_key = file_to_key("doctor_key_4")
    #desencrypted = decrypt_related_common_blocks(doc_key,cli_key.public_key(),block_chain)
    #desencrypted = get_full_history(cli_key,block_chain)
    #print(desencrypted)
    #make_new_history(cli_key,doc_key,block_chain)
