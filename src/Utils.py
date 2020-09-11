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