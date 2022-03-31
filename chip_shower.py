import json
import colorama
from colorama import Fore, Back


# define our highlight states
HSTATE_OFF = 0
HSTATE_ON = 1
HSTATE_DEFAULT = 2
HSTATE_OUT_ON = 3
HSTATE_OUT_OFF = 4

# loads a chip profile from a json file
def load_chip(fpath):
    dat = None
    with open(fpath, "r") as f:
        dat = json.load(f)
    return dat

# converts a highlight state to a color for the terminal
def get_highlight(hstate):
    if hstate == HSTATE_DEFAULT:
        return Fore.WHITE 
    elif hstate == HSTATE_ON:
        return Fore.RED + Back.GREEN
    elif hstate == HSTATE_OFF:
        return Fore.GREEN + Back.RED
    elif hstate == HSTATE_OUT_ON:
        return Fore.GREEN + Back.CYAN
    elif hstate == HSTATE_OUT_OFF:
        return Fore.CYAN + Back.RED
    else: 
        return Fore.RED

# prints the state of the chip to the terminal
def print_chip(chip, state):
    print()
    chip_size = int(len(chip["Pins"])/2)

    # top
    print(Fore.CYAN + "\t┌", end="")
    for i in range(chip_size, len(chip["Pins"])).__reversed__():
        print("─", end="")
        print(get_highlight(state[i]) + "-" + Fore.RESET + Back.RESET, end="")
        print(Fore.CYAN +"─", end="")
    print("┐")

    # body upper
    print(Fore.CYAN +"\t│", end="")
    for pin_idx in range(chip_size, len(chip["Pins"])).__reversed__():
        print(get_highlight(state[pin_idx])+f"{chip['Pins'][str(pin_idx+1)]:3}"+ Fore.RESET + Back.RESET, end="")
    print(Fore.CYAN +"│")

    # Body lower
    print(Fore.CYAN +"\t│", end="")
    for pin_idx in range(chip_size):
        print(get_highlight(state[pin_idx])+f"{chip['Pins'][str(pin_idx+1)]:3}"+ Fore.RESET + Back.RESET, end="")
    print(Fore.CYAN +"│")
    

    # bottom
    print("\t└", end="")
    for i in range(chip_size):
        print(Fore.CYAN +"─", end="")
        # print the pin state
        print(get_highlight(state[i]) + "-"+ Fore.RESET + Back.RESET, end="")
        print(Fore.CYAN +"─", end="")
    print("┘" + Fore.RESET)
    


def default_state(chip):
    hstate = []
    for _ in range(len(chip["Pins"])):
        hstate.append(HSTATE_DEFAULT)
    return hstate