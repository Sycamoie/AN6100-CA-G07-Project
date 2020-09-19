# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file is the main entry for the program

import os

from Option import Option
import Option
from Hints import welcome_hint


def main():        
    # new a instance of Option class
    options = Option()

    # init continue_flag as True
    continue_flag = True
    
    while True:
        # get user choice
        choice = input(welcome_hint).upper()

        # if choice is in the mapping
        # it is able to be handled
        if choice in options.option_mapping.keys():
            # use getattr() & dict() for handling input key mapping decently
            option_func = getattr(Option, options.option_mapping[choice])

            # option_func is function object
            continue_flag = option_func()
        else:
            print("invalid input.")

        # if option_func wants to quit the program
        if not continue_flag:
            # quit main menu
            break

    # quit the program with exit code 0
    raise SystemExit(0)


if __name__ == "__main__":   
    main()
