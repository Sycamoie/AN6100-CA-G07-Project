import os

welcome_str = \
"""
***** Foot Print Contact Point *****
D: Set Door Gate
C: Configure PC number
R : Entrance & Exit Tracking
M: Merge Input/ Output Files
Q : Quit
"""



if __name__ == "__main__":
    function = input(welcome_str)
    if function.upper() is "R":
        