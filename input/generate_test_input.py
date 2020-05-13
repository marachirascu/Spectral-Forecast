from sys import argv
import numpy as np
import random


if len(argv) < 4:
    print('Syntax:\n   python3 generate_test_input.py <INPUT_FILE> <OUTPUT_DIRECTORY> <COUNT_OUTPUTS>')
    exit(-1)

with open(argv[1], 'r') as f:
    M = [list(map(float, line.split(' '))) for line in f.read().split('\n')[:-1]]

print(M)

for n in range(int(argv[3])):
    M_new = M[::][::]
    for i in range(len(M_new)):
        for j in range(len(M_new[i])):
            M_new[i][j] += random.uniform(-2.0, 2.0)

    with open('{}/{}_{}.in'.format(argv[2], argv[2], n), 'w') as f:
        for line in M_new:
            f.write(' '.join(list(map(str, line))) + '\n')
        
