from drive import create_file_from_local, init_module, open_folder,open_sub_folder,get_file_from_folder,download_file
from file_manager import file_to_key, var_to_file,file_to_var
from watahack_bc import get_full_history, make_new_history, make_new_register,decrypt_related_common_blocks

from enum import Enum

class state(Enum):
    SET = -1

    MAIN = 0
    EXIT = 1

    ENTER_MESSAGE = 2
    ENTER_CLIENT = 3

    HISTORY = 4
    FULL = 5
    COMMON = 6
    UPDATE = 7

def client_input(input_):
    try:
        client = int(input_)
        if(client>= 0 and client <=4):
            return True
        else:
            print("Invalid Client!")
            return False
    except:
        print("Invalid Client!")
        return False

current_state = state.SET

current_message = ""
#doctorKey = file_to_key("doctor_key_0")
drive = init_module()
main_folder = open_folder(drive,"watahack_folder1")
hospital_folder = open_sub_folder(drive, main_folder, "Node_1")
BC_file = get_file_from_folder(drive,hospital_folder,"my_block_chain")

while(current_state != state.EXIT):
    if current_state == state.SET:
        input_ = input('Enter Doctor Key: ')
        try:
            doctorKey = file_to_key(input_)
            current_state = state.MAIN
            download_file(drive,BC_file,'temp')
            BC = file_to_var('temp')
        except:
            print("Invalid Key!!")

    elif(current_state == state.MAIN):
        input_ = input('Enter command: ')
        if(input_ == 'q' or input_ == 'quit'):
            current_state = state.EXIT
        elif(input_ == 'n' or input_ == 'newreg'):
            current_state = state.ENTER_MESSAGE
        elif(input_ == 'h' or input_ == 'history'):
            current_state = state.HISTORY
        elif(input_ == 'r' or input_ == 'reset'):
            current_state = state.SET
    elif(current_state == state.ENTER_MESSAGE):
        current_message = input("Enter new register: ")
        current_state = state.ENTER_CLIENT
    elif(current_state == state.ENTER_CLIENT):
        input_ = input('Enter Client Key: ')
        valid = client_input(input_)
        if valid:
            clientKey = file_to_key("client_key_%s"%(str(int(input_))))
            reg = make_new_register(current_message,doctorKey,clientKey)
            var_to_file(reg,"NewReg")
            create_file_from_local(drive,hospital_folder,"NewReg")
            print("New register sent!!!\n")
            current_state = state.MAIN
    elif(current_state == state.HISTORY):
        input_ = input("\n1) Full history\n2) Common history\n3) Previous history (update with own key)\n")
        if input_ == '1':
            current_state = state.FULL
        elif input_ == '2':
            current_state = state.COMMON
        elif input_ == '3':
            current_state = state.UPDATE
        else:
            print("Invalid option")
    elif current_state == state.FULL:
        input_ = input('Enter client Private Key: ')
        valid = client_input(input_)
        if valid:
            clientKey = file_to_key("client_key_%s"%(str(int(input_))))
            print(get_full_history(clientKey,BC))
            current_state = state.MAIN
    elif current_state == state.COMMON:
        input_ = input('Enter client Public Key: ')
        valid = client_input(input_)
        if valid:
            clientKey = file_to_key("client_key_%s"%(str(int(input_))))
            print(decrypt_related_common_blocks(doctorKey,clientKey.public_key(),BC))
            current_state = state.MAIN
    elif current_state == state.UPDATE:
        input_ = input('Enter client Private Key: ')
        valid = client_input(input_)
        if valid:
            clientKey = file_to_key("client_key_%s"%(str(int(input_))))
            reg = make_new_history(clientKey,doctorKey,BC)
            var_to_file(reg,"NewReg")
            create_file_from_local(drive,hospital_folder,"NewReg")
            print("New history created!!!\n")
            current_state = state.MAIN
    else:
        current_state = state.MAIN
