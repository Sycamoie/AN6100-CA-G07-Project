# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file contains some util functions which are reuseable

def acceptInteger1To99(question, error):
    print(question)
    pc_no = input('>>>> ')
    if pc_no.isdigit():
        if int(pc_no) in range(1, 100):
            return int(pc_no)
    print(error)
    return -1

def acceptNRIC():
    while True:
        print("Please input your NRIC number")
        nric_no = input('>>>> ')
        print('typed: ', nric_no)
        if len(nric_no) == 0 or nric_no == 'Q':
            # TODO: simplify this
            if len(nric_no) == 0:
                print("Press enter again to quit\n")
                if len(input('>>>> ')) != 0:
                    print("This is not a valid NRIC number")
                    continue
            return ''
        elif nric_no[0] in 'STFG' and len(nric_no) == 9:
            if nric_no[1:-1].isdigit() and nric_no[-1].isalpha():
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
    # check if length is 1 or 2 
    if len(chars) not in range(1, 3):
        # invalid if fail in check
        return False

    # check if is chars
    for char in chars:
        # if is char and no (isalnum)
        if char.isalnum():
            continue
        # invalid if fail in check
        else:
            return False

    # valid if passed the test
    return True