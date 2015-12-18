#!/usr/bin/python

"""
This is the subroutine at index 6027. From the book in the office, I understand
that I need to find a value of c (r7 or 32775) that produces a certain answer.

From 5491 I see that the value I'm looking for is 6.
"""

def magic(a, b, c):

    if a == 0:
        return (b + 1) % 32768

    else:
        if b == 0:
            return magic(a - 1, c, c)
        else:
            return magic(a - 1, magic(a, b -1, c), c)
            
if __name__=="__main__":
    for c in range(32768):
        output = magic(4, 1, c)
        if output==6:
            print c
