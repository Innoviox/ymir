from visualizer.constants import TileType

from collections import defaultdict
from random import choices
from math import log

transition_matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
probabilities = defaultdict(int)

def neighbors(i, j, matrix):
    max_x, max_y = len(matrix[0]), len(matrix)
    for (dx, dy) in [[-1, -1], [-1, 0], [-1, 1],
                     [ 0, -1],          [ 0, 1],
                     [ 1, -1], [ 1, 0], [ 1, 1]]:
        a, b = j + dy, i + dx
        if 0 <= a < max_y and 0 <= b < max_x:
            yield (dx, dy), matrix[a][b]
with open("visualizer/levels/test_file_3.txt") as f:
    theme, *lines = f.readlines()

    lines = [[TileType.from_tile(i) for i in j.strip()] for j in lines]
        
    for i, line in enumerate(lines):
        for j, tile in enumerate(line):
            probabilities[tile] += 1
            for (dA, n) in neighbors(i, j, lines):
                transition_matrix[tile][dA][n] += 1

class WaveFunction:
    def __init__(self, pos):
        self.position = pos
        self.reset()
        
    def entropy(self):
        sum_of_weights = 0
        sum_of_weight_log_weights = 0

        for i in self.possible:
            weight = self.coefficients[i]
            if weight > 0:
                sum_of_weights += weight        
                sum_of_weight_log_weights += weight * log(weight)

        return log(sum_of_weights) - (sum_of_weight_log_weights / sum_of_weights)

    def collapse(self):
        self.possible = choices(self.possible, self.coefficients.values())

    def __str__(self):
        if len(self.possible) > 1:
            return ' ' + str(len(self.possible)).zfill(2) + ' '
        if len(self.possible) == 1:
            return '  ' + self.possible[0].char + ' '
        return ' CN '

    def reset(self):
        self.possible = list(TileType)
        self.coefficients = {i: probabilities.get(i, 0) for i in TileType}
    
height = 15
width = 15
wave_functions = [[WaveFunction((i, j)) for i in range(width)] for j in range(height)]

entropy = lambda i: 1000 if len(i.possible) <= 1 else i.entropy()

def collapse():
    wave = min([min(i, key=entropy) for i in wave_functions], key=entropy)

    wave.collapse()

    chosen = wave.possible[0]

    for (dA, n) in neighbors(*wave.position, wave_functions):
        d = transition_matrix[chosen][dA]

        for i in n.possible[:]:
            if i not in d:
                n.possible.remove(i)
        n.coefficients = {k: v for k, v in d.items() if k in n.possible}

        if len(n.possible) == 0:
            return False
    return True

def print_functions():
    s = ''
    for i in wave_functions:
        for j in i:
            s += str(j)
        s += '\n'
    print(s)

def done():
    return all(map(lambda i: all(map(lambda x: len(x.possible) == 1, i)), wave_functions))

def reset():
    for i in wave_functions:
        for j in i:
            j.reset()

while True:
    while not done():
        if not collapse():
            print("con")
            reset()

    print_functions()
    input()
    
