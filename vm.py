#!/usr/bin/python

import numpy
import sys

class VirtualMachine():
    
    def __init__(self, debug=False):
        print "Booting MnesisVM..."
        self.memory = numpy.zeros((32775,), dtype=numpy.dtype("<u2")) # Includes the registers 
        self.stack = []
        self.running = False
        self.program_counter = 0
        self.debug = debug
        print "Ready to go!"

    def load_program(self, filename):
        print "Loading program: %s" % (filename,)
        program = numpy.fromfile(filename.encode(), dtype=numpy.dtype("<u2"))
        self.memory[0:len(program)] = program.copy()
        print "Program loaded."

    def run(self):
        print "\nRunning program:"
        self.running = True
        print "--------------------S T A R T--------------------"
        while self.running:
            if self.debug==True:
                next_op = self.memory[self.program_counter]
                print "DEBUG *** PC: %s, OP: %s, ARGS:" % (self.program_counter, VirtualMachine.debug_values[next_op]["name"]),
                print self.memory[self.program_counter+1: self.program_counter + VirtualMachine.debug_values[next_op]["args"] + 1] 
            VirtualMachine.opcodes[self.memory[self.program_counter]](self)
        print "-------------------- H A L T --------------------"

    def halt(self): # OPCODE 0
        """ Stops the program from running. """
        self.program_counter += 1
        self.running = False

    def jmp(self): # OPCODE 6
        """ Moves to the instruction pointed to by the first operand. """
        self.program_counter = self.memory[self.program_counter+1]

    def jt(self): # OPCODE 7
        """ If a is not 0, jump to b. """
        if self.memory[self.program_counter+1] != 0:
            self.program_counter = self.memory[self.program_counter+2]
        else:
            self.program_counter += 3

    def jf(self): # OPCODE 8
        """ If a is 0, jump to b. """
        if self.memory[self.program_counter+1] == 0:
            self.program_counter = self.memory[self.program_counter+2]
        else:
            self.program_counter += 3

    def out(self): # OPCODE 19
        """ Writes a single character to the console. """
        sys.stdout.write(chr(self.memory[self.program_counter+1]))
        sys.stdout.flush()
        self.program_counter += 2

    def noop(self): # OPCODE 21
        """ Does nothing. """
        self.program_counter += 1

    opcodes = {0: halt,
               6: jmp,
               7: jt,
               8: jf,
               19: out,
               21: noop,
               }

    debug_values = {0: {"name": "halt",
                        "args": 0},
                    6: {"name": "jmp",
                        "args": 1},
                    7: {"name": "jt",
                        "args": 2},
                    8: {"name": "jf",
                        "args": 2},
                    19: {"name": "out",
                         "args": 1},
                    21: {"name": "noop",
                         "args": 0},
                    }

if __name__=="__main__":

    vm = VirtualMachine(debug=False)
    vm.load_program("challenge.bin")
    vm.run()
    vm.run()
