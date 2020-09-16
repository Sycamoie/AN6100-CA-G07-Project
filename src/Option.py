# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains the main implementation for the program

from datetime import datetime

import Hints
from merge import merge_file
from Utils import *

PCno = -1
gateID = '.'

option_mapping = {
    'C': "option_c",
    'D': "option_d",
    'M': "option_m",
    'Q': "option_q",
    'R': "option_r"
}


# *********************************
# Option C
# *********************************
def option_c():
    PC_num = acceptInteger1To99("Please enter PC Number (1 to 99)",
                                "Invalid entry, please enter any number from 1 to 99 only")
    if PC_num != -1:
        global PCno
        PCno = PC_num

    # Do not quit the program
    return True


# *********************************
# Option D
# *********************************
def option_d():
    global gateID
    gateID = acceptDoorGate()

    # Do not quit the program
    return True


# *********************************
# Option M
# *********************************
def option_m():
    merge_file('./INOUT', 'merged_output.csv')
    # do not quit the program
    return True


# *********************************
# Option Q
# *********************************
def option_q():
    # quit the program
    return False


# *********************************
# Option R
# *********************************
def option_r():
    # Q4.a
    # if write failed, return to menu
    if not writeGateIDToTxt(gateID):
        return True

    # Q4.b
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

    # Q4.g
    while True:
        # get current time
        time = datetime.now()
        # # ? test with different time
        # time = datetime.strptime("2020-08-08 08:21", r"%Y-%m-%d %H:%M")
        
        # Q4.c
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

        # Q4.d
        # get mode
        mode = acceptMode()
        if mode == 'Q':
            break
        elif mode == 'e':
            # Q4.e
            # add contact number to the line
            line.append(acceptContactNo())
        elif mode == '':
            print('invalid mode!\n')
            continue

        # Q4.f
        writeDataToCSV(mode, line)

    # do not quit the program
    return True

# *********************************
# Option template
# *********************************
# def option_x():
#    # return True if the program continues
#    # return False if the program needs to break
#    return True