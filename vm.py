#!/usr/bin/python

import numpy
import sys

class VirtualMachine():
    
    def __init__(self):
        print "Booting MnesisVM..."
        self.memory = numpy.zeros((32775,), dtype=numpy.dtype("<u2")) # Includes the registers 
        self.stack = []
        self.running = False
        self.program_counter = 0
        print "Ready to go!"

    def load_program(self, filename):
        print "Loading program: %s" % (filename,)
        program = numpy.fromfile(filename.encode(), dtype=numpy.dtype("<u2"))
        self.memory[0:len(program)] = program.copy()
        print "Program loaded."

    def run(self):
        print "Running program:"
        self.running = True
        print "--------------------S T A R T--------------------"
        while self.running:
            VirtualMachine.opcodes[self.memory[self.program_counter]](self)
        print "-------------------- H A L T --------------------"

    def halt(self): # OPCODE 0
        """ Stops the program from running. """
        self.running = False

    def jmp(self): # OPCODE 6
        """ Moves to the instruction pointed to by the first operand. """
        self.program_counter = self.memory[self.program_counter+1]

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
               19: out,
               21: noop}


if __name__=="__main__":

    vm = VirtualMachine()
    vm.load_program("challenge.bin")
    vm.run()
