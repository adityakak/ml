import sys;

args = sys.argv[1:]
import time

# args = ['25', 'R13', 'R3:5 ', 'R9:6', 'R11:12', 'B16', 'B17', 'B11']
args = ['25', 'r10', 'r14']
import math
import re

size = 0
width = 0
height = 0
reward = 12
perimeter_reward = -1

game_map = [[{}]]  # Data is Dict (Reward (int), LinksTo (set), LinksFrom(set))


def twoToOne(i, j):
    return (i * width) + j


def oneToTwo(index):
    return index // width, index % width


def greedy_dir(matrix, reward_nodes):
    dir_matrix = [[None] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            if twoToOne(i, j) not in reward_nodes:
                n = game_map[i][j]['LinksTo']
                max_value = float('-inf')
                max_n = float('-inf')
                for k in n:
                    r, c = oneToTwo(k)
                    if matrix[r][c] > max_value:
                        max_value = matrix[r][c]
                        max_n = k
                dir_matrix[i][j] = direction_to_letter(twoToOne(i, j), max_n)
            else:
                dir_matrix[i][j] = "*"
    return dir_matrix


def bootstrap_dp():
    gamma = .6

    value_matrix = [[0] * width for _ in range(height)]
    value_dir = [['x'] * width for _ in range(height)]
    prev_matrix = [[None] * width for _ in range(height)]
    prev_dir = [[None] * width for _ in range(height)]

    reward_nodes = set()
    for i in range(height):
        for j in range(width):
            value_matrix[i][j] = game_map[i][j]['Reward']
            if game_map[i][j]['Reward'] != 0:
                reward_nodes.add(twoToOne(i, j))

    while prev_dir != value_dir:
        prev_dir = [row[:] for row in value_dir]
        for i in range(height):
            for j in range(width):
                if twoToOne(i, j) not in reward_nodes:
                    curr_value = 0
                    n = game_map[i][j]['LinksTo']
                    for k in n:
                        r, c = oneToTwo(k)
                        if k in reward_nodes:
                            curr_value += game_map[r][c]['Reward']
                        else:
                            curr_value += gamma * value_matrix[r][c]
                    value_matrix[i][j] = (1 / len(n)) * curr_value
        value_dir = greedy_dir(value_matrix, reward_nodes)
        print("".join([j for i in value_dir for j in i]))

def monte_carloES():



def letters_symbol(letters):
    if len(letters) == 0:
        return '.'
    elif letters == 'U':
        return 'U'
    elif letters == 'D':
        return 'D'
    elif letters == 'L':
        return 'L'
    elif letters == 'R':
        return 'R'
    elif re.search("^[U|R][R|U]$", letters):
        return 'V'
    elif re.search("^[D|L][D|L]$", letters):
        return 'E'
    elif re.search("^[U|L][U|L]$", letters):
        return 'M'
    elif re.search("^[D|R][D|R]$", letters):
        return 'S'
    elif re.search("^[D|U][D|U]$", letters):
        return '|'
    elif re.search("^[R|L][R|L]$", letters):
        return '-'
    elif re.search("^[U|R|D][U|R|D][U|R|D]$", letters):
        return 'W'
    elif re.search("^[U|L|D][U|L|D][U|L|D]$", letters):
        return 'F'
    elif re.search("^[U|R|L][U|R|L][U|R|L]$", letters):
        return 'N'
    elif re.search("^[L|R|D][L|R|D][L|R|D]$", letters):
        return 'T'
    elif letters == '*':
        return letters
    elif letters == '0':
        return '.'
    else:
        return '+'


def toggle_direction(cell, directions):
    row, col = oneToTwo(cell)
    neigh = []
    for direction in directions:
        if direction == 'E':
            if col + 1 < width:
                neigh.append((row * width) + col + 1)
                # toggle_link(cell, (row * width) + col + 1)
        elif direction == 'W':
            if col - 1 >= 0:
                neigh.append((row * width) + col - 1)
                # toggle_link(cell, (row * width) + col - 1)
        elif direction == 'N':
            if row - 1 >= 0:
                neigh.append(((row - 1) * width) + col)
                # toggle_link(cell, ((row - 1) * width) + col)
        else:
            if row + 1 < height:
                neigh.append(((row + 1) * width) + col)
                # toggle_link(cell, ((row + 1) * width) + col)
    for n in neigh:
        if n in game_map[row][col]['LinksTo']:
            toggle_link(cell, n, False)
        else:
            toggle_link(cell, n, True)


def toggle_link(cell, n, on):
    global game_map
    row, col = oneToTwo(cell)
    if on:
        game_map[row][col]['LinksTo'].add(n)
        game_map[row][col]['LinksFrom'].add(n)
        game_map[n // width][n % width]['LinksTo'].add(cell)
        game_map[n // width][n % width]['LinksFrom'].add(cell)
    else:
        game_map[row][col]['LinksTo'].remove(n)
        game_map[row][col]['LinksFrom'].remove(n)
        game_map[n // width][n % width]['LinksTo'].remove(cell)
        game_map[n // width][n % width]['LinksFrom'].remove(cell)


def toggle_links(cell):
    global game_map
    row, col = oneToTwo(cell)
    neigh = direction_neighbors(cell)
    for n in neigh:
        if n in game_map[row][col]['LinksTo']:
            toggle_link(cell, n, False)
        else:
            toggle_link(cell, n, True)


def direction_to_letter(cell, n):
    row, col = oneToTwo(cell)
    if n == ((row + 1) * width) + col:
        return 'D'
    elif n == ((row - 1) * width) + col:
        return 'U'
    elif n == (row * width) + col - 1:
        return 'L'
    else:
        return 'R'


def direction_neighbors(cell):
    neigh = []
    row, col = oneToTwo(cell)
    if row + 1 < height:
        neigh.append(((row + 1) * width) + col)
    if row - 1 >= 0:
        neigh.append(((row - 1) * width) + col)
    if col - 1 >= 0:
        neigh.append((row * width) + col - 1)
    if col + 1 < width:
        neigh.append((row * width) + col + 1)
    return neigh


def neighbors(cell):
    global game_map
    row, col = oneToTwo(cell)
    neigh = direction_neighbors(cell)
    game_map[row][col]['LinksTo'] = set(neigh)
    for k in neigh:
        game_map[k // width][k % width]["LinksFrom"].add(cell)
    return neigh


def process_input(string):
    global reward, perimeter_reward, game_map, args
    if re.search('^R:\d$', string, flags=re.IGNORECASE):
        reward = int(string[string.find(":") + 1:])
    elif re.search('^R::', string, flags=re.IGNORECASE):
        perimeter_reward = int(string[string.rfind(":") + 1:])
    elif re.search('^R\d+$', string, flags=re.IGNORECASE):
        cell = int(string[1:])
        game_map[cell // width][cell % width]['Reward'] = reward
    elif re.search('^R\d+:\d+$', string, flags=re.IGNORECASE):
        cell = int(string[string.find("R") + 1:string.find(":")])
        local_reward = int(string[string.find(":") + 1:])
        game_map[cell // width][cell % width]['Reward'] = local_reward
    elif re.search('^B\d+$', string, flags=re.IGNORECASE):
        cell = int(string[string.find("B") + 1:])
        toggle_links(cell)
    elif re.search('^B\d+\w', string, flags=re.IGNORECASE):
        last_digit = re.match('.+([0-9])[^0-9]*$', string)
        cell = int(string[string.find("B") + 1:last_digit.start(1) + 1])
        directions = string[last_digit.start(1) + 1:]
        toggle_direction(cell, directions)


def main():
    global width, height, size, game_map, args
    start_index = 1
    size = int(args[0])
    if len(args) > 1 and args[1].isdigit():
        width = int(args[1])
        height = size // width
        start_index += 1
    else:
        sqrt_ans = math.ceil(size ** .5)
        while size % sqrt_ans != 0:
            sqrt_ans += 1
        width = sqrt_ans
        height = size // width
    game_map = [x[:] for x in [[None] * width] * height]
    for i in range(height):
        for j in range(width):
            game_map[i][j] = {"Reward": 0, "LinksTo": set(), "LinksFrom": set()}
    for i in range(height):
        for j in range(width):
            neighbors((i * width) + j)
    for i in range(start_index, len(args)):
        process_input(args[i])
    bootstrap_dp()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)

# Aditya Kak 3 2022
