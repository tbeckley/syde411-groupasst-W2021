import random
from sys import argv

mydict = {}

NUM_CASES = int(argv[1])

if argv[2] == "knapsack": 
    for i in range(1, NUM_CASES+1):
        val = round(random.random()*5, 2) + 0.1
        mydict[i] = (val, round(val * random.random() * 25, 2))

    print(mydict)

elif argv[2] == "ts":
    KP_MATRIX = [None] * NUM_CASES
    for i in range(NUM_CASES):
        KP_MATRIX[i] = [0] * NUM_CASES

    for i in range(NUM_CASES):
        for j in range(i+1, NUM_CASES):
            val = round(random.random()*100)

            KP_MATRIX[i][j] = val
            KP_MATRIX[j][i] = val

    print(KP_MATRIX)

