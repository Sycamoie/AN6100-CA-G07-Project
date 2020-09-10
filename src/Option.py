from src.Utils import *

#*********************************
# Option C
#*********************************
def option_c():
    PCno = Utils.acceptInteger1To99("Please enter PC Number (1 to 99)", "Invalid entry, please enter any number from 1 to 99 only")
    print(PCno, 'correct!') if PCno != -1 else ''

#*********************************
# Option R
#*********************************
def option_r():
    from src.Hints import *
    door_gate_ID = ''

    while True:
        if door_gate_ID:
            break
        else:
            door_gate_ID = input(f"\n{input_gate_hint}{return_to_menu}>>>> ")
            if isChar(door_gate_ID):
                print('True')
            else:
                print(f"invalid door gate id{return_to_menu}")
                continue
        with open("ID-DoorGate.txt", 'a+') as door_gate_record:
            print(door_gate_ID, file=door_gate_record)
    
    if globals()['PCno'] == -1:
        option_c()