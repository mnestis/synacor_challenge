#!/usr/bin/python

import numpy
import sys

def load_program(filename):
    return numpy.fromfile(filename.encode(), dtype=numpy.dtype("<u2"))
    
def export_program(program, filename):
    file = open(filename, "w")
    i = 0
    while i < len(program):
        try:
            file.write(str(i) + ": " + debug_values[program[i]]["name"] + " ")
            file.write(str(program[i+1:i+1+debug_values[program[i]]["args"]]))
            i += 1 + debug_values[program[i]]["args"]
        except KeyError:
            file.write(str(i) + ": " + "Memory value " + str(program[i]))
            i += 1
        file.write("\n")
        file.flush()
 
    file.close()

debug_values = {0: {"name": "halt",
                    "args": 0},
                1: {"name": "set",
                    "args": 2},
                2: {"name": "push",
                    "args": 1},
                3: {"name": "pop",
                    "args": 1},
                4: {"name": "eq",
                    "args": 3},
                5: {"name": "gt",
                    "args": 3},
                6: {"name": "jmp",
                    "args": 1},
                7: {"name": "jt",
                    "args": 2},
                8: {"name": "jf",
                    "args": 2},
                9: {"name": "add",
                    "args": 3},
                10: {"name": "mult",
                     "args": 3},
                11: {"name": "mod",
                     "args": 3},
                12: {"name": "and",
                     "args": 3},
                13: {"name": "or",
                     "args": 3},
                14: {"name": "not",
                     "args": 2},
                15: {"name": "rmem",
                     "args": 2},
                16: {"name": "wmem",
                     "args": 2},
                17: {"name": "call",
                     "args": 1},
                18: {"name": "ret",
                     "args": 0},
                19: {"name": "out",
                     "args": 1},
                20: {"name": "in",
                     "args": 1},
                21: {"name": "noop",
                     "args": 0},
                }

if __name__=="__main__":
    
    program = load_program("challenge.bin")
    export_program(program, "code.asm")
