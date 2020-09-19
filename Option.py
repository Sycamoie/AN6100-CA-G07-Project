# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains the main implementation for the program

from datetime import datetime
<<<<<<< Updated upstream:src/Option.py
from Utils import *
import Hints
import os

=======
import os

from merge import merge_file
# DO NOT use wildcard import or else it will mess the global
from Utils import acceptInteger1To99, acceptDoorGate, writeGateIDToTxt, \
    writePCNoToTxt, acceptNRIC, acceptMode, acceptContactNo, writeDataToCSV
>>>>>>> Stashed changes:Option.py

PCno = -1
gateID = '.'

<<<<<<< Updated upstream:src/Option.py
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
        PC_no = acceptInteger1To99("Please enter PC Number (1 to 99)", "Invalid entry, please enter any number from 1 to 99 only")
        if PC_no != -1:
            global PCno
            PCno = PC_no

        # Do not quit the program
        return True
=======
# the key mapping for main menu and functions
option_mapping = {
    # if new option to be added
    # 'user input': "function_name",
    # 'X': "option_x",
    'C': "option_c",
    'D': "option_d",
    'M': "option_m",
    'Q': "option_q",
    'R': "option_r"
}


# *********************************
# Option X
# *********************************
# def option_x():
#    # return True if the program continues
#    # return False if the program needs to break
#    return True


# *********************************
# Option C
# *********************************
# Projection Specification 5
def option_c():
    pc_num = acceptInteger1To99("Please enter PC Number (1 to 99)",
                                "Invalid entry, please enter any number from 1 to 99 only")
    if pc_num != -1:
        global PCno
        PCno = pc_num

    # Do not quit the program
    return True

>>>>>>> Stashed changes:Option.py

#*********************************
# Option D
<<<<<<< Updated upstream:src/Option.py
#*********************************
    @staticmethod
    def option_d():
        door_gate_ID = '.'
        # TODO: move to Utils
        while True:
            print(Hints.enter_gateID_hint)
            door_gate_ID = input(">>>> ")
            if isGateID(door_gate_ID):
                break
            else:
                continue
        global gateID
        gateID = door_gate_ID

        # Do not quit the program
        return True
=======
# *********************************
# Projection Specification 6
def option_d():
    global gateID
    gateID = acceptDoorGate()

    # Do not quit the program
    return True

>>>>>>> Stashed changes:Option.py

#*********************************
# Option M
<<<<<<< Updated upstream:src/Option.py
#*********************************
    @staticmethod
    def option_m():
        # raise UnimplementedError()
        # do not quit the program
        return True
=======
# *********************************
# Projection Specification 9
def option_m():
    merge_file('./INOUT', './', 'merged_output.csv')
    # do not quit the program
    return True

>>>>>>> Stashed changes:Option.py

#*********************************
# Option Q
<<<<<<< Updated upstream:src/Option.py
#*********************************
    @staticmethod
    def option_q():
        # quit the program
        return False
=======
# *********************************
# Projection Specification 3
def option_q():
    # quit the program
    return False

>>>>>>> Stashed changes:Option.py

#*********************************
# Option R
<<<<<<< Updated upstream:src/Option.py
#*********************************
    @classmethod
    def option_r(self):
        # Q4.a
        # # TODO: just check validity here.
        # # !IMPORTANT: This should be fixed
        # if gateID == '.':
        #     self.option_d()
        if not isGateID(gateID):
            input(Hints.invalid_gate_hint)
            return True
        with open("ID-DoorGate.txt", 'w') as door_gate_record:
            door_gate_record.write(str(gateID))
        
        # Q4.b
        while PCno == -1:
            self.option_c()
        with open("ID-PCNumber.txt", 'w') as pc_number_record:
            pc_number_record.write(str(PCno).zfill(2))

        print("The system time will be used for record")
        print(datetime.now())

        # if the INOUT dir not exist, create it
        if not os.path.exists("./INOUT"):
            try:
                os.makedirs("./INOUT")
            except Exception:
                print("unable to create dir 'INOUT'")

        # Q4.c
        while True:
            # get current time
            # time = datetime.now()
            # ? test with different time
            time = datetime.strptime("2020-08-08 08:21", r"%Y-%m-%d %H:%M")

            # get nric
            nric_no = acceptNRIC()
            if nric_no == '':
                break

            # format a line of data
            line = [time.strftime(r"%Y-%m-%d"), 
                    time.strftime(r"%H:%M"),
                    str(gateID),
                    str(PCno).zfill(2),
                    nric_no] 

            # get mode
            mode = acceptMode()
            if mode == 'Q':
                break
            elif mode == 'e':
                # add contact number to the line
                line.append(acceptContactNo())

            # csv starts with IN or OT
            csv_name = ["IN" if mode == 'e' else "OT"]
            # then date
            csv_name.append(time.strftime(r"%Y%m%d"))
            # then gate ID
            csv_name.append(str(gateID))
            # then PC Number
            csv_name.append(str(PCno).zfill(2))
            # then hour number
            csv_name.append(time.strftime("%H00").zfill(4))

            # concat into the file name
            csv_name = '_'.join(csv_name)
            # add affix to format full path
            csv_name = './INOUT/'+csv_name+'.csv'

            # add header if csv not exists
            header =  not os.path.exists(csv_name)
            print("Header: ", header)

            with open(csv_name, "a+") as csv_out:
                if header:
                # if the file does not exist
                    print("adding header")
                    # add headers to it
                    if mode == 'e':
                        # in header
                        print(','.join(Header_IN), file=csv_out)
                    elif mode == 'x':
                        # out header
                        print(','.join(Header_OT), file=csv_out)

                # write the line to csv_out
                print(','.join(line), file=csv_out)
        
        # do not quit the program
        return True
=======
# *********************************
# Projection Specification 4
def option_r():
    # Projection Specification 4.a
    # if write failed, return to menu
    if not writeGateIDToTxt(gateID):
        return True

    # Projection Specification 4.b
    global PCno
    while PCno == -1:
        PCno = acceptInteger1To99("Please enter PC Number (1 to 99)",
                                  "Invalid entry, please enter any number from 1 to 99 only\n")
    writePCNoToTxt(PCno)

    # if the INOUT dir not exist, create it
    if not os.path.exists("./INOUT"):
        try:
            os.makedirs("./INOUT")
        except Exception as e:
            print("unable to create sub-dir 'INOUT'\ncaused by ", e)

    # Projection Specification 4.g
    while True:
        # get current time
        time = datetime.now()
        # # ? test with different time
        # time = datetime.strptime("2020-08-08 08:21", r"%Y-%m-%d %H:%M")

        # Projection Specification 4.c
        # get nric
        nric_no = acceptNRIC()
        if nric_no == '':
            break

        # format a line of data
        line = [time.strftime(r"%Y-%m-%d"),
                time.strftime(r"%H:%M"),
                str(gateID),
                str(PCno).zfill(2),
                nric_no]

        # Projection Specification 4.d
        # get mode
        mode = acceptMode()
        if mode == 'Q':
            break
        elif mode == 'e':
            # Projection Specification 4.e
            # add contact number to the line
            line.append(acceptContactNo())
        elif mode == '':
            print('invalid mode!\n')
            continue

        # Projection Specification 4.f
        writeDataToCSV(mode, line)

    # do not quit the program
    return True
>>>>>>> Stashed changes:Option.py
