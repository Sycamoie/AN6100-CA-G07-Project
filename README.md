# AN6100-CA-G07-Project

## _Description_
> __NTU AN6100 Class A Group 07 Group Project__

----
## Roadmap

### C 
> _Configure PC NO_
* acceptInteger1To99(question, error)

ask for input with `question` as the hint. check if the `input` is a number between 1 and 99. If valid, assign to the global variable `PCno`. If invalid, print the `error` message.

|@param||
|----|----|
|question| The input hint for asking PC No. (an int)|
|error| The output error message if received invalid input|

`global PCno` : PCno should be a global variable

### D
> _Set Door Gate_
* isValidGateID(gate_id)

ask for input. check if is valid (hint: use `str.isalnum()`). use `while True` for looping until valid input is received.
Assign to global variable `gateID`.

|@param||
|----|----|
|gate_id| The variable to be checked for validity|

|@return||
|----|----|
|validity| if gate_id is a valid gate ID|

`global gateID` : gateID should be a global variable

### M
> _Merge Input/Output files_

* mergeOutput()

merge all .csv file in the /INOUT directory into one .csv file which should be stored in the __HOME__ directory.
compute the `StayMinsDuration`

### Q
> quit

change the flag inside the loops

### R
> tracking

* saveToFile(var, filename)

check if gateID and PCno exists or else invoke method to receive input

|@param||
|----|----|
|var| The variable to be saved, namely `gateID` & `PCno`|
|filename| The filename for opening and saving|

<br/>

>
>Then, use keyboard to scan in the ID
>
>receive choice for next step
>
>- `e: Entrance`
>- `x: Exit`
>- `Q: Quit`
>
>enter contact no if in `Entrance` mode
>
>save the data into csv files

loop above steps. When Q is entered, break and return to the main menu

----
## Miscellaneous

### FILE

>In

__File name format__

IN_YYYYMMDD\_[GATE]\_[PC]\_[startTime].csv

__Columns__

* Date
* TimeIn
* GateIn
* PCIn
* NRIC
* ContactNo

>Out

__File name format__

OT_YYYYMMDD\_[GATE]\_[PC]\_[startTime].csv

__Columns__

* Date
* TimeOut
* GateOut
* PCOut
* NRIC

>Merge

__File name format__

merged_output.csv

__Columns__

* Date
* In Time
* In Gate
* In PC
* ContactNo
* Out Gate
* Out Time
* Out PC
* StayMinsDuration