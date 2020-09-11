# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains the main implementation for the program

import Utils
import Hints

PCno = -1
gateID = '.'

class Option:
    def __init__(self):
        self.option_mapping = {
            'C': "option_c",
            'D': "option_d",
            'M': "option_m",
            'Q': "option_q",
            'R': "option_r"
        }

#*********************************
# Option C
#*********************************
    @staticmethod
    def option_c():
        PC_no = Utils.acceptInteger1To99("Please enter PC Number (1 to 99)", "Invalid entry, please enter any number from 1 to 99 only")
        if PC_no == -1:
            pass
        global PCno
        PCno = PC_no

        # Do not quit the program
        return True

#*********************************
# Option D
#*********************************
    @staticmethod
    def option_d():
        door_gate_ID = '.'
        while True:
            print(Hints.enter_gateID_hint)
            door_gate_ID = input(">>>> ")
            if Utils.isGateID(door_gate_ID):
                break
            else:
                continue
        global gateID
        gateID = door_gate_ID

        # Do not quit the program
        return True

#*********************************
# Option M
#*********************************
    @staticmethod
    def option_m():
        # raise Utils.UnimplementedError()
        # do not quit the program
        return True

#*********************************
# Option Q
#*********************************
    @staticmethod
    def option_q():
        # quit the program
        return False

#*********************************
# Option R
#*********************************
    @classmethod
    def option_r(self):
        # TODO: replace with option_d
        while True:
            if gateID != '.':
                break
            else:
                print(f"{Hints.input_gate_hint}{Hints.return_menu_hint}")
                door_gate_ID = input(">>>> ")
                if Utils.isGateID(door_gate_ID):
                    print('True')
                elif door_gate_ID.upper() == 'QUIT':
                    break
                else:
                    print(f"invalid door gate id{Hints.return_menu_hint}")
                    continue
            with open("ID-DoorGate.txt", 'a+') as door_gate_record:
                print(door_gate_ID, file=door_gate_record)
        if PCno == -1:
            self.option_c()
        
        # do not quit the program
        return True