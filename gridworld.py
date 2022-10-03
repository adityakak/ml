import sys; args = sys.argv[1:]
import math
import re

#
args = ["25", "r2", "r22", "G0"]
# args = sys.argv[:1]

# args = ['25', 'R13', 'R3:5', 'R9:6', 'R11:12', 'B16', 'B17', 'B11', 'G1']
# args = ['30', 'B14', '', 'G0']
# args = ['30', '5','R6:7', 'R23:8', 'G0']
# args = ['30', 'R6:7', "R23:8", "G1"]

size = 0
width = 0
height = 0
reward = 12
perimeter_reward = -1

game_map = [[{}]]  # Data is Tuple (Reward (int), LinksTo (set), LinksFrom(set))


def twoToOne(i, j):
    return (i * width) + j


def oneToTwo(index):
    return index // width, index % width


def bfs_distance(cell):
    depth = {cell: 0}
    explored = {cell}
    nodes = [(cell, 0)]
    while len(nodes) > 0:
        node = nodes.pop(0)
        for n in game_map[node[0] // width][node[0] % width]['LinksTo']:
            if n not in explored and game_map[n // width][n % width]['Reward'] == 0:
                nodes.append((n, node[1] + 1))
                depth[n] = node[1] + 1
                explored.add(n)
    return depth


def g0_search():
    direction = [x[:] for x in [[("", float('-inf'))] * width] * height]
    locations = []
    for i in range(height):
        for j in range(width):
            if game_map[i][j]['Reward'] > 0:
                locations.append([game_map[i][j]['Reward'], twoToOne(i, j)])
    locations.sort(key=lambda x: x[0], reverse=True)
    for loc in locations:
        loc.append(bfs_distance(loc[1]))  # Reward Amount, Cell of Reward, Distance Map
    for i in range(height):
        for j in range(width):
            if game_map[i][j]['Reward'] > 0:
                direction[i][j] = "*"
            else:
                for loc in locations:
                    distance_map = loc[2]
                    answer = ""
                    if loc[0] >= direction[i][j][1] and twoToOne(i, j) in distance_map:
                        for neigh in game_map[i][j]['LinksTo']:
                            if neigh == loc[1] or (
                                    game_map[neigh // width][neigh % width]['Reward'] == 0 and distance_map[neigh] ==
                                    distance_map[twoToOne(i, j)] - 1):
                                answer += direction_to_letter(twoToOne(i, j), neigh)
                        direction[i][j] = (answer + direction[i][j][0], loc[0])
    for i in range(height):
        for j in range(width):
            print(letters_symbol("".join(set(direction[i][j][0]))), end=' ')
        print()


def g1_search():
    direction = [x[:] for x in [[("", float('-inf'))] * width] * height]
    locations = []
    for i in range(height):
        for j in range(width):
            if game_map[i][j]['Reward'] > 0:
                locations.append([game_map[i][j]['Reward'], twoToOne(i, j)])
    for loc in locations:
        loc.append(bfs_distance(loc[1]))  # Reward Amount, Cell of Reward, Distance Map
    for i in range(height):
        for j in range(width):
            if game_map[i][j]['Reward'] > 0:
                direction[i][j] = "*"
            else:
                for loc in locations:
                    distance_map = loc[2]
                    answer = ""
                    if twoToOne(i, j) in distance_map and loc[0] / distance_map[twoToOne(i, j)] >= direction[i][j][1]:
                        ratio = loc[0] / distance_map[twoToOne(i, j)]
                        for neigh in game_map[i][j]['LinksTo']:
                            try:
                                if neigh == loc[1] or (
                                        game_map[neigh // width][neigh % width]['Reward'] == 0 and distance_map[
                                    neigh] == distance_map[twoToOne(i, j)] - 1):
                                    answer += direction_to_letter(twoToOne(i, j), neigh)
                            except KeyError:
                                print()
                        if ratio == direction[i][j][1]:
                            direction[i][j] = (answer + direction[i][j][0], ratio)
                        else:
                            direction[i][j] = (answer, ratio)
    for i in range(height):
        for j in range(width):
            print(letters_symbol("".join(set(direction[i][j][0]))), end=' ')
        print()


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
        """
        first_cell = int(string[string.find("R") + 1:string.find(":")])
        second_cell = int(string[string.find(":") + 1:])
        game_map[second_cell // width][second_cell % width]['Reward'] = \
            game_map[first_cell // width][first_cell % width]['Reward']
        """
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
    elif re.search('^G\d$', string, flags=re.IGNORECASE):
        if string[1] == '0':
            g0_search()
        else:
            g1_search()


def main():
    global width, height, size, game_map, args
    #args = args[0].split(" ")
    #print(args)
    start_index = 1
    size = int(args[0])
    if args[1].isdigit():
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
    search = None  # G0 True G1 False
    for i in range(start_index, len(args)):
        if args[i] == 'G0':
            search = True
        elif args[i] == 'G1':
            search = False
        else:
            process_input(args[i])
    if search:
        process_input("G0")
    else:
        process_input("G1")
    print("======")


if __name__ == "__main__":
    main()

# Aditya Kak 3 2022
