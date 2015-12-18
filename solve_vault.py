#!/usr/bin/python

import random

def solve_vault():

    vault = [["22", "+", "4", "*"],
             ["-", "4", "*", "8"],
             ["9", "-", "11", "-"],
             ["*", "18", "*", "1"]]

    routes = []

    while True:
        count = 0
        x = 0
        y = 0
        value = "22"
        while count <= 12:
            dir = random.randint(0,3)
            if dir == 0 and x != 0:
                x -= 1
            elif dir == 1 and x != 3:
                x += 1
            elif dir == 2 and y != 0:
                y -= 1
            elif dir == 3 and y != 3:
                y += 1
            else:
                continue
            value += vault[x][y]
            if (y + x) % 2 == 0:
                value = "("+value+")"
            
            if x == 0 and y == 0:
                break

            if x == 3 and y == 3:
                orb_mass = eval(value)
                if orb_mass == 30:
                    if value not in routes:
                        routes.append(value)
                        print value
                else:
                    break
            count += 1
    


if __name__=="__main__":
    print solve_vault()
