# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains some util functions which are reusable
from Hints import invalid_gate_hint, enter_gateID_hint
import os
import re

Header_IN = ["Date", "Time", "Gate", "PC", "NRIC", "ContactNo"]
Header_OT = ["Date", "Time", "Gate", "PC", "NRIC"]


def acceptInteger1To99(question, error):
    print(question)
    pc_no = input('>>>> ')
    if pc_no.isdigit():
        if int(pc_no) in range(1, 100):
            return int(pc_no)
    print(error)
    return -1


def acceptDoorGate():
    door_gate_ID = '.'
    while True:
        print(enter_gateID_hint)
        door_gate_ID = input(">>>> ")
        if isGateID(door_gate_ID):
            return door_gate_ID

def acceptNRIC():
    while True:
        print("Please input your NRIC number")
        nric_no = input('>>>> ')
        if len(nric_no) == 0 or nric_no == 'Q':
            if len(input("Press enter again to quit  ")) != 0:
                print("Invalid input")
                continue
            return ''
        elif isNRIC(nric_no):
            return nric_no
        print("This is not a valid NRIC number")


def acceptMode():
    print("Please input the mode")
    mode = input('>>>> ')
    if mode in 'eQx':
        return mode
    else: 
        return ''


def acceptContactNo():
    while True:
        print("Please input your contact number")
        contact_no = input('>>>> ')
        if len(contact_no) == 8 and contact_no[0] in '89' and contact_no.isdigit():
            return contact_no
        print("invalid contact number")


def isGateID(chars):
    # gate ID should be alphanumeric
    # length within 2
    if re.match(r'\s*[0-9a-z]{1,2}$', chars, flags=re.IGNORECASE):
        # return True if valid
        return True
    else:
        return False


def isNRIC(nric):
    # check NRIC string pattern
    # length of 9
    # start with one of S T F G
    # follow by 7 numbers
    # end with a char
    if re.match(r'\s*[STFG]\d{7}\w', nric, flags=re.IGNORECASE):
        # return True if valid
        return True
    else:
        return False


def writeGateIDToTxt(gateID):
    if not isGateID(gateID):
        input(invalid_gate_hint)
        return False
    with open("ID-DoorGate.txt", 'w') as door_gate_record:
        door_gate_record.write(str(gateID))
    return True


def writePCNoToTxt(PCno):
    with open("ID-PCNumber.txt", 'w') as pc_number_record:
        pc_number_record.write(str(PCno).zfill(2))


# def writeDataToCSV(mode, line):
#     pass
def writeDataToCSV(mode, line):
    # csv starts with IN or OT
    # then date, gate ID, PC Number, hour number
    csv_name = ["IN" if mode == 'e' else "OT",
                line[0].replace("-", ""),
                line[2],
                line[3],
                f"{line[1].split(':')[0].zfill(2)}00"]

    # concat into the file name
    csv_name = '_'.join(csv_name)
    # add affix to format full path
    csv_name = './INOUT/'+csv_name+'.csv'
    # same day file name
    csv_name_of_same_day = './INOUT/' + '_'.join(csv_name[:-1])

    # as one file per day
    # to make sure that the file for today is not created
    # walk thru the INOUT path
    for file in os.listdir('./INOUT'):
        # if the file name with different time already exists
        if file.startswith(csv_name_of_same_day):
            # write to that file
            csv_name = './INOUT/' + file

    # add header if csv not exists
    header = not os.path.exists(csv_name)

    with open(csv_name, "a+") as csv_out:
        # if the file does not exist
        if header:
            # add headers to it
            if mode == 'e':
                # in header
                print(','.join(Header_IN), file=csv_out)
            elif mode == 'x':
                # out header
                print(','.join(Header_OT), file=csv_out)

        # write the line to csv_out
        print(','.join(line), file=csv_out)
