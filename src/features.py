import re
pcnum = 0

# validat gate id, return a false message if the gate id is not valid


def check_gate_id(gate_id):
    pattern = r'[A-Z0-9]{2}'
    regex = re.compile(pattern, flags=re.IGNORECASE)
    while(regex.fullmatch(gate_id) == None):
        input(
            "Please enter a valud door gate before recording visits, press any key to return to the menu: ")
        break


def valid_pc():
    pattern = r'[0-9]{2}'
    regex = re.compile(pattern)
    while regex.fullmatch(pcnum) == None:
        # call the set pc fucntion
        pass


def get_id():
    id = None
    while(not(id is None)):
        id = input('Please scan your ID: ')


check_gate_id('[5')
