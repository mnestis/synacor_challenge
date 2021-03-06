#!/usr/bin/python

import numpy
import sys
import pickle

class VirtualMachine():
    
    def __init__(self, debug=False, log=None):
        self.memory = numpy.zeros((32776,), dtype=numpy.dtype("<u2")) # Includes the registers 
        self.stack = []
        self.running = False
        self.program_counter = 0
        self.debug = debug
        self.logfile = log
        self.log("MnestisVM ready to go!")

    def load_program(self, filename):
        self.log("Loading program: %s" % (filename,))
        program = numpy.fromfile(filename.encode(), dtype=numpy.dtype("<u2"))
        self.memory[0:len(program)] = program.copy()
        self.log("Program loaded.")

    def run(self):
        self.log("\nRunning program:")
        self.running = True
        self.log("--------------------S T A R T--------------------")
        while self.running:
            if self.debug==True:
                next_op = self.memory[self.program_counter]
                self.log("PC: %s, OP: %s, ARGS: " % (self.program_counter, VirtualMachine.debug_values[next_op]["name"]),
                         str(self.memory[self.program_counter+1: self.program_counter + VirtualMachine.debug_values[next_op]["args"] + 1]), 
                         "Reg: " + str(self.memory[32768:]),
                         "Stack:" + str(self.stack))
            VirtualMachine.opcodes[self.memory[self.program_counter]](self)
        self.log("-------------------- H A L T --------------------")

    def log(self, *msgs):
        if not debug:
            return
        for msg in msgs:
            self.logfile.write(str(msg))
        self.logfile.write("\n")
        self.logfile.flush()

    def dump(self, dump_loc):
        dump_file = open(dump_loc, "w")
        dump_file.write(pickle.dumps({"memory": self.memory,
                                      "stack": self.stack,
                                      "program_counter": self.program_counter}))
        dump_file.flush()

    def load_dump(self, dump_loc):
        dump_file = open(dump_loc, "r")
        contents = pickle.loads(dump_file.read())
        self.memory = contents["memory"]
        self.stack = contents["stack"]
        self.program_counter = contents["program_counter"]
        dump_file.close()

    def get_arg(self, index):
        arg = self.memory[self.program_counter + index]
        if arg >= 32768:
            arg = self.memory[arg]
        return arg

    def get_register(self, index):
        return self.memory[self.program_counter + index]

    def halt(self): # OPCODE 0
        """ Stops the program from running. """
        self.program_counter += 1
        self.running = False

    def set(self): # OPCODE 1
        """ Sets register a to value of b """
        self.memory[self.get_register(1)] = self.get_arg(2)
        self.program_counter += 3

    def push(self): # OPCODE 4
        self.stack.append(self.get_arg(1))
        self.program_counter += 2

    def pop(self): # OPCODE 3
        """ Pop an item from the stack, if there is one, error if there's not. """
        self.memory[self.get_register(1)] = self.stack.pop()
        self.program_counter += 2

    def eq(self): # OPCODE 4
        """ a=1 if b==c else a=0 """
        self.memory[self.get_register(1)] = 1 if self.get_arg(2) == self.get_arg(3) else 0
        self.program_counter += 4

    def gt(self): # OPCODE 5
        """ a=1 if b>c else a=0 """
        self.memory[self.get_register(1)] = 1 if self.get_arg(2) > self.get_arg(3) else 0
        self.program_counter += 4

    def jmp(self): # OPCODE 6
        """ Moves to the instruction pointed to by the first operand. """
        self.program_counter = self.get_arg(1)

    def jt(self): # OPCODE 7
        """ If a is not 0, jump to b. """
        
        if self.get_arg(1) != 0:
            self.program_counter = self.get_arg(2)
        else:
            self.program_counter += 3

    def jf(self): # OPCODE 8
        """ If a is 0, jump to b. """
        if self.get_arg(1) == 0:
            self.program_counter = self.get_arg(2)
        else:
            self.program_counter += 3

    def add(self): # OPCODE 9
        """ a=b+c """
        self.memory[self.get_register(1)] = (self.get_arg(2) + self.get_arg(3)) % 32768
        self.program_counter += 4

    def mult(self): # OPCODE 10
        """ a=b*c """
        self.memory[self.get_register(1)] = (int(self.get_arg(2)) * int(self.get_arg(3))) % 32768
        self.program_counter += 4

    def mod(self): # OPCODE 11
        """ a = b%c """
        self.memory[self.get_register(1)] = self.get_arg(2) % self.get_arg(3)
        self.program_counter += 4

    def bitwise_and(self): # OPCODE 12
        """ a = b&c """
        self.memory[self.get_register(1)] = self.get_arg(2) & self.get_arg(3)
        self.program_counter += 4

    def bitwise_or(self): # OPCODE 13
        """ a = b|c """
        self.memory[self.get_register(1)] = self.get_arg(2) | self.get_arg(3)
        self.program_counter += 4

    def bitwise_not(self): # OPCODE 14
        """ a = not b"""
        # This one's a bit more complicated, because we can't just use the standard not operator
        self.memory[self.get_register(1)] = self.get_arg(2) ^ 32767
        self.program_counter += 3

    def rmem(self): # OPCODE 15
        """ Copy from b to a """
        self.memory[self.get_register(1)] = self.memory[self.get_arg(2)]
        self.program_counter += 3

    def wmem(self): # OPCODE 15
        """ Write b to a """
        self.memory[self.get_arg(1)] = self.get_arg(2)
        self.program_counter += 3

    def call(self): # OPCODE 17
        """ Push pc+1 to stack, branch to a """
        self.stack.append(self.program_counter+2)
        self.program_counter = self.get_arg(1)

    def ret(self): # OPCODE 18
        """ Pop from stack and jump to it """
        if len(self.stack) != 0:
            self.program_counter = self.stack.pop()
        else:
            self.halt()    

    def out(self): # OPCODE 19
        """ Writes a single character to the console. """
        sys.stdout.write(chr(self.get_arg(1)))
        sys.stdout.flush()
        self.program_counter += 2

    def char_in(self): # OPCODE 20
        """ Read in a single character from the console. """
        self.memory[self.get_register(1)] = ord(sys.stdin.read(1))
        self.program_counter += 2

    def noop(self): # OPCODE 21
        """ Does nothing. """
        self.program_counter += 1

    opcodes = {0: halt,
               1: set,
               2: push,
               3: pop,
               4: eq,
               5: gt,
               6: jmp,
               7: jt,
               8: jf,
               9: add,
               10: mult,
               11: mod,
               12: bitwise_and,
               13: bitwise_or,
               14: bitwise_not,
               15: rmem,
               16: wmem,
               17: call,
               18: ret,
               19: out,
               20: char_in,
               21: noop,
               }

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
    from sys import argv

    if len(argv) > 2:
        debug = True
        log_filename = argv[2]
        log_file = open(log_filename, "w+")
    else:
        debug = False
        log_file = None

    vm = VirtualMachine(debug=debug, log=log_file)
    
    if len(argv) > 1:
        vm.load_dump(argv[1])
    else:
        vm.load_program("challenge.bin")

    try:
        vm.run()
    except KeyboardInterrupt:
        dump_p = raw_input("Dump memory? (y/N): ")
        if dump_p.lower() == "y":
            dump_loc = raw_input("Where would you like to dump it? ")
            vm.dump(dump_loc)
            
