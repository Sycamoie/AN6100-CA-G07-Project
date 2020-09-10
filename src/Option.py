import Utils
import Hints

PCno = -1
gateID = '.'

#*********************************
# Option C
#*********************************
def option_c():
    PC_no = Utils.acceptInteger1To99("Please enter PC Number (1 to 99)", "Invalid entry, please enter any number from 1 to 99 only")
    if PC_no == -1:
        pass
    global PCno
    PCno = PC_no

#*********************************
# Option D
#*********************************
def option_d():
    door_gate_ID = '.'
    while True:
        print(Hints.enter_gateID_hint)
        door_gate_ID = input(">>>> ")
        if Utils.isGateID(door_gate_ID):
            break
        else:
            continue
    global gateID
    gateID = door_gate_ID

#*********************************
# Option R
#*********************************
def option_r():
    while True:
        if gateID != '.':
            break
        else:
            print(f"{Hints.input_gate_hint}{Hints.return_menu_hint}")
            door_gate_ID = input(">>>> ")
            if Utils.isGateID(door_gate_ID):
                print('True')
            else:
                print(f"invalid door gate id{Hints.return_menu_hint}")
                continue
        with open("ID-DoorGate.txt", 'a+') as door_gate_record:
            print(door_gate_ID, file=door_gate_record)
    if PCno == -1:
        option_c()