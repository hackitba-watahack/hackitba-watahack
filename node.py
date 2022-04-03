from drive import init_module,open_folder,create_file_from_local,get_list_from_folder,download_file,change_content_from_string, open_sub_folder, get_file_from_folder, change_content_from_file
from file_manager import var_to_file, file_to_var, key_to_file, file_to_key
from watahack_bc import is_register_on_block_chain, regType, validate_register
from enum import Enum

class state(Enum):
    MAIN = 0
    EXIT = 1

    VERIFYING = 2

current_state = state.MAIN

drive = init_module()
main_folder = open_folder(drive,"watahack_folder1")
hospital_folder = open_sub_folder(drive, main_folder, "Node_1")
BC_file = get_file_from_folder(drive,hospital_folder,"my_block_chain")
download_file(drive,BC_file,"my_block_chain")
block_chain = file_to_var("my_block_chain")

peer_folder = open_sub_folder(drive,main_folder, "Node_2")

while(current_state != state.EXIT):
    if(current_state == state.MAIN):
        input_ = input('Enter command: ')
        if(input_ == 'q' or input_ == 'quit'):
            current_state = state.EXIT
        elif(input_ == 'v' or input_ == 'verify'):
            current_state = state.VERIFYING
        elif(input_ == 's' or input_ == 'size'):
            print(len(block_chain))
    elif(current_state == state.VERIFYING):
        file_ = get_file_from_folder(drive, hospital_folder, "NewReg")
        if file_ != 0:
            download_file(drive,file_,"NewReg")
            newreg = file_to_var("NewReg")
            if validate_register(newreg):# and not is_register_on_block_chain(newreg,block_chain):
                block_chain.append(newreg)
                var_to_file(block_chain,"my_block_chain")
                change_content_from_file(BC_file,"my_block_chain")
                print("New register verified!!!")

                create_file_from_local(drive,peer_folder,"NewReg")
            #elif is_register_on_block_chain(newreg,block_chain):
            #    print("Register already on BlockChain")
            else:
                print("Fraudulent register detected")
            file_.Delete()
        else:
            current_state = state.MAIN
