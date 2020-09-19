# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains some util functions which are reusable
from Hints import invalid_gate_hint, enter_gateID_hint, mode_selection_hint
import os
import re

# headers for csv files
Header_IN = ["Date", "TimeIn", "GateIn", "PCIn", "NRIC", "ContactNo"]
Header_OT = ["Date", "TimeOut", "GateOut", "PCOut", "NRIC"]


def acceptInteger1To99(question: str, error: str) -> int:
    """
    ask for input a PC number from user with `question`

    if invalid, print error and return -1

    :param question: input hint
    :param error: the error message if an invalid input
    :return: the input pc number if valid or -1 if invalid
    """
    print(question)
    pc_no = input('>>>> ').strip()
    if pc_no.isdigit():
        if int(pc_no) in range(1, 100):
            return int(pc_no)
    print(error)
    return -1


def acceptDoorGate():
    """
    use INFINITE loop to accept a Door Gate

    :return: a valid door gate
    """
    while True:
        print(enter_gateID_hint)
        door_gate_id = input('>>>> ').strip()
        if isGateID(door_gate_id):
            return door_gate_id


def acceptNRIC() -> str:
    """
    use INFINITE loop to accept a NRIC code

    can quit by enter Q and enter, then confirm again with enter

    :return: NRIC if success or blank string if failed
    """
    while True:
        # ask for inputs
        print("Please input your NRIC number")
        nric_no = input('>>>> ').strip()

        # if nothing is inputted
        if len(nric_no) == 0:
            # ask for pressing enter again
            if len(input("Press enter again to quit  ")) != 0:
                # if user enter something else, do not quit
                print("Invalid input")
                continue
            return ''
        # quit directly if enter Q for NRIC
        elif nric_no == 'Q':
            return ''
        # check if is valid NRIC no
        elif isNRIC(nric_no):
            return nric_no
        # if not, inform user of invalidity
        else:
            print("This is not a valid NRIC number")


def acceptMode():
    """
    accept input from user of the mode

    - e: entrance

    - x: exit

    - Q: quit

    :return: mode or blank string if failed
    """
    while True:
        # ask for mode input
        print(mode_selection_hint)
        mode = input('>>>> ').strip()

        # if input is valid, just return
        if mode in 'eQx':
            return mode
        # else inform
        else:
            print("invalid mode! Please input again. Use capital Q if wants quitting")
            continue


def acceptContactNo():
    """
    use INFINITE loop to get a valid contact number

    :return: a valid contact number
    """
    while True:
        print("Please input your contact number")
        contact_no = hasContactNo(input('>>>> ').strip())
        if contact_no:
            return contact_no
        print("invalid contact number")


def isGateID(gate: str) -> bool:
    """
    use regular expression to validate gate ID, which should follow:

    - length of 2

    - all should be alphanumeric characters

    example:

        A, 2, A2, 22    valid

        $, ^, (>, <)    invalid

    :param gate: the gateID to be validated
    :return: validity
    """
    # gate ID should be alphanumeric
    # length within 2
    return bool(re.match(r'[0-9A-Z]{1,2}$', gate, flags=re.IGNORECASE))


def isNRIC(nric: str) -> bool:
    """
    use regular expression to validate NRIC, which should follow:

    - length of 9

    - start with one of [S T F G]

    - follow by 7 numbers

    - end with a char

    :param nric: the nric string to be validated
    :return: validity
    """
    # check NRIC string pattern
    return bool(re.match(r'[STFG]\d{7}[A-Z]$', nric, flags=re.IGNORECASE))


def hasContactNo(contact: str) -> str:
    """
    use regular expression to validate contact number, which should follow:

    - length of 8 or longer

    - starts with +65 or 65

    - follow by '-' or a blank space or nothing

    - the 8 digit number should start with one of [6 8 9]

    - may be a space between the first 4 and last 4 digit

    valid example:

    * +65-6888 8888

    * 65 88888888

    * 98888888
    :param contact: the contact number to be validated
    :return: the correct contact number
    """
    # check contact number
    # can start with country code
    contact = re.match(r'\+?(65)?[-\s]?([689]\d{3})\s?(\d{4})$', contact, flags=re.IGNORECASE)
    if contact:
        return f"{contact.group(2)}{contact.group(3)}"
    else:
        return ''


def writeGateIDToTxt(gate_id: str) -> bool:
    """
    :param gate_id: gateID to be written to ID-DoorGate.txt
    :return: success in writing or not
    """
    # if gate ID is invalid
    if not isGateID(gate_id):
        # inform the user and return to main menu with any key
        input(invalid_gate_hint)
        # did not success
        return False

    # try to write to txt
    try:
        # open ID-DoorGate.txt
        with open("ID-DoorGate.txt", 'w') as door_gate_record:
            # write one line to 1
            door_gate_record.write(str(gate_id))
            # success
            return True
    # handle system error
    # such as no access right or disk is full
    except OSError:
        # inform the user
        print("----ERROR: unable to create and write to txt file")
        # writing failed
        return False


def writePCNoToTxt(pc_no):
    """
    :param pc_no: pc number to be written to ID-PCNumber.txt
    """
    with open("ID-PCNumber.txt", 'w') as pc_number_record:
        pc_number_record.write(str(pc_no).zfill(2))


def writeDataToCSV(mode: str, line: list):
    """
    write a line of data into the targeted csv
    :param mode: 'e' entrance or 'x' exit for distinguishing the IN or OT file
    :param line: the line of data in a list format
    """
    # csv starts with IN or OT
    # then date, gate ID, PC Number, hour number
    csv_name = ["IN" if mode == 'e' else "OT",
                line[0].replace("-", ""),
                line[2],
                line[3],
                f"{line[1].split(':')[0].zfill(2)}00"]

    # same day file name
    csv_name_of_same_day = '_'.join(csv_name[:-1])
    # concat into the file name
    csv_name = '_'.join(csv_name)

    # as one file per day
    # to make sure that the file for today is not created
    # walk thru the INOUT path
    for file in os.listdir('./INOUT'):
        # if the file name with different time already exists
        if file.startswith(csv_name_of_same_day):
            # write to that file
            csv_name = './INOUT/' + file
            break
    else:
        # add affix to format full path
        csv_name = './INOUT/'+csv_name+'.csv'

    # add header if csv not exists
    header = not os.path.exists(csv_name)

    with open(csv_name, "a+") as csv_out:
        # add header if csv not exists
        if header:
            if mode == 'e':
                # in header
                print(','.join(Header_IN), file=csv_out)
            elif mode == 'x':
                # out header
                print(','.join(Header_OT), file=csv_out)

        # write the line to csv_out
        print(','.join(line), file=csv_out)
