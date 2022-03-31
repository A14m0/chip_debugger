from operator import truth
import sys
import os
import platform
import re
import colorama
from colorama import Fore

# Custom stuff
import chip_shower
import truthtable


current_chip = None

class Command:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func


########## LOADING AND UNLOADING ##########
def load(args):
    global current_chip
    try:
        current_chip = chip_shower.load_chip(args[0])
    except Exception as e:
        print(Fore.RED + f"[-] Failed to load chip profile: {str(e)}" + Fore.RESET)

def unload(args):
    global current_chip 
    current_chip = None


########## SHOWING AND CHECKING ##########
def show(args):
    # make sure we have a chip
    if current_chip == None:
        print(Fore.RED + "[-] No chip loaded, cannot show" + Fore.RESET)
        return

    hstate = chip_shower.default_state(current_chip)

    if args != []:
        # see if we are printing input states or not
        if ":" in args[0]:
            # parse the arguments
            for a in args:
                v = a.split(":")
                pin = v[0]
                nums = v[1]
                for n in range(len(nums)):
                    for k in current_chip["Pins"]:
                        if current_chip["Pins"][str(k)] == f"{pin}{n}":
                            if nums[n] == "1":
                                hstate[int(k)-1] = chip_shower.HSTATE_ON
                            else: 
                                hstate[int(k)-1] = chip_shower.HSTATE_OFF
        else:
            for arg in args:
                for pin in current_chip["Pins"]:
                    if re.search(arg, current_chip["Pins"][pin]) != None:
                        hstate[int(pin)-1] = chip_shower.HSTATE_ON
                

    chip_shower.print_chip(current_chip, hstate)

def check(args):
    # make sure we have a chip
    if current_chip == None:
        print(Fore.RED + "[-] No chip loaded, cannot show" + Fore.RESET)
        return

    hstate = chip_shower.default_state(current_chip)
    ttable = truthtable.load_table(current_chip)
    vcount = len(current_chip['TruthTable']['InputCount'] + current_chip['TruthTable']['OutputCount'])
    header = current_chip["TruthTable"]["Values"]
    

    if args != []:
        if ":" in args[0]:
            # parse the arguments
            for a in args:
                v = a.split(":")
                pin = v[0]
                nums = v[1]
                for n in range(len(nums)):
                    for k in current_chip["Pins"]:
                        if current_chip["Pins"][str(k)] == f"{pin}{n}":
                            if nums[n] == "1":
                                hstate[int(k)-1] = chip_shower.HSTATE_ON
                            else: 
                                hstate[int(k)-1] = chip_shower.HSTATE_OFF
        else:
            # sanity check arguments
            if len(args) < vcount:
                print(Fore.RED + f"[-]\tNot enough arguments ([{header}])")
                return

            key = ",".join(args[:len(current_chip['TruthTable']['InputCount'])])
            val = ",".join(args[len(current_chip['TruthTable']['InputCount']):])
            
            # check and report
            v = ttable[key] 
            if v != val:
                print(Fore.RED + f"[-]\tValue does NOT match what we expect (expected [{v}] got [{val}])")
            else:
                print(Fore.GREEN + "[+]\tValue matches expected result")


    else:
        # we have no arguments to default to interactive mode
        vals = input(Fore.CYAN + f"Need {header} > ")
        while vals != "exit":
            # convert to decimal
            vs = vals.split(" ")
            if len(vs) != vcount:
                print(Fore.RED + f"[-]\tEnter {vcount} binary numbers")
            else:

                # parse values
                key = ",".join(vs[:len(current_chip['TruthTable']['InputCount'])])
                val = ",".join(vs[len(current_chip['TruthTable']['InputCount']):])
                
                # check and report
                v = ttable[key] 
                if v != val:
                    print(Fore.RED + f"[-]\tValue does NOT match what we expect (expected [{v}] got [{val}])")
                else:
                    print(Fore.GREEN + "[+]\tValue matches expected result")

            # get next
            vals = input(Fore.CYAN + f"Need {vcount} inputs > ")
        
                

    chip_shower.print_chip(current_chip, hstate)



########## HELPER FUNCTIONS ##########
def clear(args):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def help(args):
    for f in commands:
        print(Fore.GREEN + f"{commands[f].name}"+ Fore.RESET + f"\t{commands[f].desc}")

def die(args):
    sys.exit(0)

########## COMMAND DEFINITIONS ##########
commands = {
    "load": Command("load", "Loads a chip profile from a file", load),
    "unload": Command("unload", "Unloads the current chip profile", unload),
    "show": Command("show", "Shows the current chip's pin layout. Optionally can add a regex expression to highlight specific pins", show),
    "check": Command("check", "Checks if a set of values works for the loaded chip", check),
    "clear": Command("clear", "Clears the screen", clear),
    "help": Command("help", "Shows available commands", help),
    "exit": Command("exit", "Terminates the program", die)
}


########## MAIN COMMAND LOOP ##########
def command_loop():
    while True:
        if current_chip == None:
            command_str = input(Fore.CYAN + "[] > " + Fore.RESET).split()
        else:
            command_str = input(Fore.CYAN + f"[{current_chip['Name']}] > " + Fore.RESET).split()
        
        
        if command_str[0] in commands:
            if len(command_str) > 1: 
                commands[command_str[0]].func(command_str[1:])
            else:
                commands[command_str[0]].func([])
        else:
            print(Fore.RED + f"[-] Unknown command '{command_str[0]}'. Use 'help' for a list of comands" + Fore.RESET)



if __name__ == "__main__":
    command_loop()