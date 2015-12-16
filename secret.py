#!/usr/bin/python

def magic(a, b, c):

    if a == 0:
        a = b + 1
        return a

    else:
        if b == 0:
            a -= 1
            b = c
            a = magic(a, b, c)
            return a
        else:
            b -= 1
            b = magic(a, b, c)
            a -= 1
            a = magic(a, b, c)
            return a
            

"""

A can become:
 b + 1 <= if a == 0
 magic(a-1, b, c) <= if b == 0
 magic(a-1, magic(a, b-1, c)) <= if b != 0

B can become:
 b <= if a == 0
 c <= if b == 0
 magic(a, b-1, c) <= if b != 0

If a is 0, return b + 1


Investigate 16235

"""

if __name__=="__main__":
    for c in range(256):
        output = magic(4, 1, c)
        print output
