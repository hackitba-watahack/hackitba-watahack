import drive
import encrypting

from enum import Enum

class state(Enum):
    MAIN = 0
    EXIT = 1

current_state = state.MAIN

while(current_state != state.EXIT):
    if(current_state == state.MAIN):
        input_ = input('Enter command: ')
        if(input_ == 'q' or input_ == 'quit'):
            current_state = state.EXIT
