from drive import create_file_from_local, init_module, open_folder,open_sub_folder,get_file_from_folder,download_file
from file_manager import file_to_key, var_to_file,file_to_var
from watahack_bc import make_new_register

from enum import Enum

class state(Enum):
    MAIN = 0
    EXIT = 1

    ENTER_MESSAGE = 2
    ENTER_CLIENT = 3

current_state = state.MAIN

current_message = ""
doctorKey = file_to_key("doctor_key_0")
drive = init_module()
main_folder = open_folder(drive,"watahack_folder1")
hospital_folder = open_sub_folder(drive, main_folder, "Node_1")

while(current_state != state.EXIT):
    if(current_state == state.MAIN):
        input_ = input('Enter command: ')
        if(input_ == 'q' or input_ == 'quit'):
            current_state = state.EXIT
        elif(input_ == 'n' or input_ == 'newreg'):
            current_state = state.ENTER_MESSAGE
    elif(current_state == state.ENTER_MESSAGE):
        current_message = input("Enter new register: ")
        current_state = state.ENTER_CLIENT
    elif(current_state == state.ENTER_CLIENT):
        input_ = input('Enter Client Key: ')
        try:
            client = int(input_)
            if(client>= 0 and client <=4):
                clientKey = file_to_key("client_key_%s"%(str(client)))
                reg = make_new_register(current_message,doctorKey,clientKey)
                var_to_file(reg,"NewReg")
                create_file_from_local(drive,hospital_folder,"NewReg")
                print("New register sent!!!\n")
                current_state = state.MAIN
            else:
                print("Invalid Client!")
        except:
            print("Invalid Client!")
