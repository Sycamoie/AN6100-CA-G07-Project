# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01
# This file is the main entry for the program

import os

import Option
from Hints import welcome_hint


def main():
    while True:
        # get user choice
        choice = input(welcome_hint).upper()

        # if choice is in the mapping
        # it is able to be handled
        if choice in Option.option_mapping.keys():
            # use getattr() & dict() for handling input key mapping decently
            option_func = getattr(Option, Option.option_mapping[choice])

            # option_func is function object
            # if option_func wants to quit the program, quit main menu
            if not option_func():
                break
        else:
            print("invalid input.")

    # quit the program with exit code 0
    raise SystemExit(0)


if __name__ == "__main__":   
    main()
