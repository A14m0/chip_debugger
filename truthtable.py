"""
This program can generate and check a demonstrated value against a truth table
for a 4bit + 4bit adder circuit.
"""
import sys
import colorama
from colorama import Fore


def convert_val(v):
    """Convert a table entry into a savable string"""
    # save A bits
    A0=v[0] & 0x1
    A1=(v[0] & 0x2) >> 1
    A2=(v[0] & 0x4) >> 2
    A3=(v[0] & 0x8) >> 3

    # save B bits
    B0=(v[1] & 0x1) >> 0
    B1=(v[1] & 0x2) >> 1
    B2=(v[1] & 0x4) >> 2
    B3=(v[1] & 0x8) >> 3
    
    # Save S bits
    S0=(v[3] & 0x1) >> 0
    S1=(v[3] & 0x2) >> 1
    S2=(v[3] & 0x4) >> 2
    S3=(v[3] & 0x8) >> 3
    
    
    return f"{A3},{A2},{A1},{A0},{B3},{B2},{B1},{B0},{v[2]},{S3},{S2},{S1},{S0},{v[4]}\n"


def main(save_table):
    # generate the table
    table = []
    for carry in range(0, 2):
        for i in range(0, 0x10):
            table.append([])
            for j in range(0, 0x10):
                sum_ctr = j + i + carry
                table[i+carry*0x10].append((i, j, carry, sum_ctr & 0xf, (sum_ctr & 0x10)>>4))
            
    # save the table
    if save_table:
        with open("table_dump.csv", "w") as f:
            # write header
            f.write("A3,A2,A1,A0,B3,B2,B1,B0,Cin,S3,S2,S1,S0,Cout\n")
            # write table
            for line in table:
                for v in line:
                    f.write(convert_val(v))
        print(Fore.GREEN + "[i]\tTable saved")

            


def load_table(chip):
    path = chip["TruthTable"]["File"]
    with open(path, "r") as f:
        ret = {}

        data = f.readlines()

        ret["header"] = data[0]
        data = data[1:]
        for line in data:
            tmp_inputs = []
            tmp_outputs = []
            ctr = 0
            line = line.split(',')

            # loads the inputs
            for v in chip["TruthTable"]["InputCount"]:
                tmp_inputs.append("".join(line[ctr:ctr+v]))
                ctr += v
            
            # loads the outputs
            for v in chip["TruthTable"]["OutputCount"]:
                tmp_outputs.append("".join(line[ctr:ctr+v]))
                ctr += v

            # save it
            key = ",".join(tmp_inputs)
            val = ",".join(tmp_outputs).replace('\n', '')
            ret[key] = val
                
        return ret

