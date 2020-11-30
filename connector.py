<<<<<<< HEAD
'''
File: connector.py

The following file initiates
a minesweeper board inside the CLIPS environment
'''

import clips # clipspy
import reader
import itertools

# Sets the tiles number 
def define_tiles(size, positions):
    
    tiles = set(range(size))
    radius = set(range(-1,2)) # {-1, 0, 1}
    
    # Minesweeper board representation
    tile_info = [[0 for i in range(size)] for j in range(size)]
    
    for i,j in itertools.product(tiles, tiles):
        bombs = 0
        if (i,j) in positions:
            bombs = -1
        else:
            for m, n in itertools.product(radius, radius):
                if (m,n) == (0,0) or (i+m not in tiles) or (j+n not in tiles):
                    continue
                elif (i+m, j+n) in positions:
                    bombs += 1

        tile_info[i][j] = bombs # Assign coordinates with number of bombs
    
    
    return tile_info

# Prints current state of board
def current_state(facts):

    g = [[0 for i in range(size)] for j in range(size)]
    
    for f in env.facts():
        try:
            if f['x'] >= 0:
                # print(f'({int(f["x1"])},{int(f["y1"])})')
                if f['state'] == 'open':
                    g[int(f['x'])][int(f['y'])] = int(f['bombs'])
                elif f['state'] == 'close':
                    # print(f['state'])
                    g[int(f['x'])][int(f['y'])] = -999
                elif f['state'] == 'flagged':
                    g[int(f['x'])][int(f['y'])] = -2
                else:
                    g[int(f['x'])][int(f['y'])] = 9        
        except Exception as e:
            pass
    
    for i in range(size):
        for j in range(size):
            if g[i][j] == -999:
                print('█', end=" ")
            elif g[i][j] == -2:
                print('F', end=" ")
            else:
                print(g[i][j], end=" ")
        print()

if __name__ == "__main__":

    env = clips.Environment()
    env.load('minesweeper.clp')
    env.reset()

    size, total, positions = reader.read_board_file('tc4.txt')

    # Defines the board size and total number of mines
    poss = list(range(size))
    pospos = "nil "
    for i in range(size):
        pospos += f"{i} "
    pospos += "nil"
    
    board_fact = f'(board (size {size}) (total-mines {total}))'

    env.assert_string(board_fact)

    info = define_tiles(size, positions)
    for i in range(size):
        for j in range(size):
            tiles_fact = f'(tile (x {i}) (y {j}) (bombs {info[i][j]}) (state close))'
            env.assert_string(tiles_fact)
            env.assert_string(f'(flag-around (x {i}) (y {j}) (num 0))')

        # PRINTS BOARD TO TERMINAL ##
            if (i,j) not in positions:
                print(info[i][j], end=" ")
            else:
                print("X", end=" ")
        print()

    # for f in env.facts():
    #     print(f)
    # r = env.find_rule("after-flag")
    # r.add_breakpoint()
    
    # for i in range(10):
    env.run()
    f = env.facts()
    current_state(f)
    print("-------------")
    
    # print("-------------")
    # for f in env.facts():
    #     print(f)

    f = env.facts()
    current_state(f)
=======
39,39,39,13,10,70,105,108,101,58,32,99,111,110,110,101,99,116,111,114,46,112,121,13,10,13,10,84,104,101,32,102,111,108,108,111,119,105,110,103,32,102,105,108,101,32,105,110,105,116,105,97,116,101,115,13,10,97,32,109,105,110,101,115,119,101,101,112,101,114,32,98,111,97,114,100,32,105,110,115,105,100,101,32,116,104,101,32,67,76,73,80,83,32,101,110,118,105,114,111,110,109,101,110,116,13,10,39,39,39,13,10,13,10,105,109,112,111,114,116,32,99,108,105,112,115,32,35,32,99,108,105,112,115,112,121,13,10,105,109,112,111,114,116,32,114,101,97,100,101,114,13,10,105,109,112,111,114,116,32,105,116,101,114,116,111,111,108,115,13,10,105,109,112,111,114,116,32,115,121,115,13,10,13,10,105,109,112,111,114,116,32,116,107,105,110,116,101,114,32,97,115,32,116,107,13,10,13,10,67,76,79,83,69,68,32,61,32,45,57,57,57,13,10,70,76,65,71,71,69,68,32,61,32,45,50,13,10,13,10,35,32,83,101,116,115,32,116,104,101,32,116,105,108,101,115,32,110,117,109,98,101,114,32,13,10,100,101,102,32,100,101,102,105,110,101,95,116,105,108,101,115,40,115,105,122,101,44,32,112,111,115,105,116,105,111,110,115,41,58,13,10,32,32,32,32,13,10,32,32,32,32,116,105,108,101,115,32,61,32,115,101,116,40,114,97,110,103,101,40,115,105,122,101,41,41,13,10,32,32,32,32,114,97,100,105,117,115,32,61,32,115,101,116,40,114,97,110,103,101,40,45,49,44,50,41,41,32,35,32,123,45,49,44,32,48,44,32,49,125,13,10,32,32,32,32,13,10,32,32,32,32,35,32,77,105,110,101,115,119,101,101,112,101,114,32,98,111,97,114,100,32,114,101,112,114,101,115,101,110,116,97,116,105,111,110,13,10,32,32,32,32,116,105,108,101,95,105,110,102,111,32,61,32,91,91,48,32,102,111,114,32,105,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,93,32,102,111,114,32,106,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,93,13,10,32,32,32,32,13,10,32,32,32,32,102,111,114,32,105,44,106,32,105,110,32,105,116,101,114,116,111,111,108,115,46,112,114,111,100,117,99,116,40,116,105,108,101,115,44,32,116,105,108,101,115,41,58,13,10,32,32,32,32,32,32,32,32,98,111,109,98,115,32,61,32,48,13,10,32,32,32,32,32,32,32,32,105,102,32,40,105,44,106,41,32,105,110,32,112,111,115,105,116,105,111,110,115,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,98,111,109,98,115,32,61,32,45,49,13,10,32,32,32,32,32,32,32,32,101,108,115,101,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,102,111,114,32,109,44,32,110,32,105,110,32,105,116,101,114,116,111,111,108,115,46,112,114,111,100,117,99,116,40,114,97,100,105,117,115,44,32,114,97,100,105,117,115,41,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,105,102,32,40,109,44,110,41,32,61,61,32,40,48,44,48,41,32,111,114,32,40,105,43,109,32,110,111,116,32,105,110,32,116,105,108,101,115,41,32,111,114,32,40,106,43,110,32,110,111,116,32,105,110,32,116,105,108,101,115,41,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,99,111,110,116,105,110,117,101,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,101,108,105,102,32,40,105,43,109,44,32,106,43,110,41,32,105,110,32,112,111,115,105,116,105,111,110,115,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,98,111,109,98,115,32,43,61,32,49,13,10,13,10,32,32,32,32,32,32,32,32,116,105,108,101,95,105,110,102,111,91,105,93,91,106,93,32,61,32,98,111,109,98,115,32,35,32,65,115,115,105,103,110,32,99,111,111,114,100,105,110,97,116,101,115,32,119,105,116,104,32,110,117,109,98,101,114,32,111,102,32,98,111,109,98,115,13,10,32,32,32,32,13,10,32,32,32,32,13,10,32,32,32,32,114,101,116,117,114,110,32,116,105,108,101,95,105,110,102,111,13,10,13,10,35,32,80,114,105,110,116,115,32,99,117,114,114,101,110,116,32,115,116,97,116,101,32,111,102,32,98,111,97,114,100,13,10,100,101,102,32,99,117,114,114,101,110,116,95,115,116,97,116,101,40,102,97,99,116,115,41,58,13,10,13,10,32,32,32,32,103,32,61,32,91,91,48,32,102,111,114,32,105,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,93,32,102,111,114,32,106,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,93,13,10,32,32,32,32,13,10,32,32,32,32,102,111,114,32,102,32,105,110,32,101,110,118,46,102,97,99,116,115,40,41,58,13,10,32,32,32,32,32,32,32,32,116,114,121,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,105,102,32,102,91,39,120,39,93,32,62,61,32,48,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,105,102,32,102,91,39,115,116,97,116,101,39,93,32,61,61,32,39,111,112,101,110,39,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,103,91,105,110,116,40,102,91,39,120,39,93,41,93,91,105,110,116,40,102,91,39,121,39,93,41,93,32,61,32,105,110,116,40,102,91,39,98,111,109,98,115,39,93,41,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,101,108,105,102,32,102,91,39,115,116,97,116,101,39,93,32,61,61,32,39,99,108,111,115,101,39,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,103,91,105,110,116,40,102,91,39,120,39,93,41,93,91,105,110,116,40,102,91,39,121,39,93,41,93,32,61,32,67,76,79,83,69,68,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,101,108,105,102,32,102,91,39,115,116,97,116,101,39,93,32,61,61,32,39,102,108,97,103,103,101,100,39,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,103,91,105,110,116,40,102,91,39,120,39,93,41,93,91,105,110,116,40,102,91,39,121,39,93,41,93,32,61,32,70,76,65,71,71,69,68,13,10,32,32,13,10,32,32,32,32,32,32,32,32,101,120,99,101,112,116,32,69,120,99,101,112,116,105,111,110,32,97,115,32,101,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,112,97,115,115,13,10,32,32,32,32,13,10,32,32,32,32,35,32,77,101,110,97,109,112,105,108,107,97,110,32,104,97,115,105,108,32,111,112,101,114,97,115,105,32,97,103,101,110,32,109,105,110,101,115,119,101,101,112,101,114,32,112,97,100,97,32,108,97,121,97,114,13,10,32,32,32,32,102,111,114,32,105,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,58,13,10,32,32,32,32,32,32,32,32,102,111,114,32,106,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,105,102,32,103,91,105,93,91,106,93,32,61,61,32,45,57,57,57,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,112,114,105,110,116,40,39,226,150,136,39,44,32,101,110,100,61,34,32,34,41,13,10,32,32,32,32,32,32,32,32,32,32,32,32,101,108,105,102,32,103,91,105,93,91,106,93,32,61,61,32,45,50,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,112,114,105,110,116,40,39,70,39,44,32,101,110,100,61,34,32,34,41,13,10,32,32,32,32,32,32,32,32,32,32,32,32,101,108,115,101,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,112,114,105,110,116,40,103,91,105,93,91,106,93,44,32,101,110,100,61,34,32,34,41,13,10,32,32,32,32,32,32,32,32,112,114,105,110,116,40,41,13,10,13,10,13,10,105,102,32,95,95,110,97,109,101,95,95,32,61,61,32,34,95,95,109,97,105,110,95,95,34,58,13,10,13,10,32,32,32,32,35,32,83,101,116,117,112,32,101,110,118,105,114,111,110,109,101,110,116,32,67,76,73,80,83,32,13,10,32,32,32,32,101,110,118,32,61,32,99,108,105,112,115,46,69,110,118,105,114,111,110,109,101,110,116,40,41,13,10,32,32,32,32,101,110,118,46,108,111,97,100,40,39,109,105,110,101,115,119,101,101,112,101,114,46,99,108,112,39,41,13,10,32,32,32,32,101,110,118,46,114,101,115,101,116,40,41,13,10,32,32,32,32,13,10,32,32,32,32,115,105,122,101,44,32,116,111,116,97,108,44,32,112,111,115,105,116,105,111,110,115,32,61,32,48,44,32,48,44,32,91,93,13,10,13,10,32,32,32,32,105,102,32,108,101,110,40,115,121,115,46,97,114,103,118,41,32,60,32,50,58,13,10,32,32,32,32,32,32,32,32,115,105,122,101,44,32,116,111,116,97,108,44,32,112,111,115,105,116,105,111,110,115,32,61,32,114,101,97,100,101,114,46,114,101,97,100,95,98,111,97,114,100,40,41,13,10,32,32,32,32,101,108,115,101,58,13,10,32,32,32,32,32,32,32,32,115,105,122,101,44,32,116,111,116,97,108,44,32,112,111,115,105,116,105,111,110,115,32,61,32,114,101,97,100,101,114,46,114,101,97,100,95,98,111,97,114,100,95,102,105,108,101,40,115,121,115,46,97,114,103,118,91,49,93,41,13,10,13,10,32,32,32,32,35,32,68,101,102,105,110,101,115,32,116,104,101,32,98,111,97,114,100,32,115,105,122,101,32,97,110,100,32,116,111,116,97,108,32,110,117,109,98,101,114,32,111,102,32,109,105,110,101,115,13,10,32,32,32,32,98,111,97,114,100,95,102,97,99,116,32,61,32,102,39,40,98,111,97,114,100,32,40,115,105,122,101,32,123,115,105,122,101,125,41,32,40,116,111,116,97,108,45,109,105,110,101,115,32,123,116,111,116,97,108,125,41,41,39,13,10,13,10,32,32,32,32,35,32,65,115,115,101,114,116,115,32,98,111,97,114,100,32,115,105,122,101,32,97,110,100,32,116,111,116,97,108,45,109,105,110,101,115,32,116,111,32,116,104,101,32,101,110,118,13,10,32,32,32,32,101,110,118,46,97,115,115,101,114,116,95,115,116,114,105,110,103,40,98,111,97,114,100,95,102,97,99,116,41,13,10,13,10,32,32,32,32,35,32,65,115,115,105,103,110,115,32,101,97,99,104,32,116,105,108,101,115,32,119,105,116,104,32,116,104,101,32,99,111,114,114,101,115,112,111,110,100,105,110,103,32,118,97,108,117,101,32,98,97,115,101,100,32,111,110,13,10,32,32,32,32,35,32,116,104,101,32,110,117,109,98,101,114,32,111,102,32,98,111,109,98,115,13,10,32,32,32,32,105,110,102,111,32,61,32,100,101,102,105,110,101,95,116,105,108,101,115,40,115,105,122,101,44,32,112,111,115,105,116,105,111,110,115,41,13,10,32,32,32,32,13,10,32,32,32,32,102,111,114,32,105,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,58,13,10,32,32,32,32,32,32,32,32,102,111,114,32,106,32,105,110,32,114,97,110,103,101,40,115,105,122,101,41,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,116,105,108,101,115,95,102,97,99,116,32,61,32,102,39,40,116,105,108,101,32,40,120,32,123,105,125,41,32,40,121,32,123,106,125,41,32,40,98,111,109,98,115,32,123,105,110,102,111,91,105,93,91,106,93,125,41,32,40,115,116,97,116,101,32,99,108,111,115,101,41,41,39,13,10,32,32,32,32,32,32,32,32,32,32,32,32,101,110,118,46,97,115,115,101,114,116,95,115,116,114,105,110,103,40,116,105,108,101,115,95,102,97,99,116,41,13,10,32,32,32,32,32,32,32,32,32,32,32,32,101,110,118,46,97,115,115,101,114,116,95,115,116,114,105,110,103,40,102,39,40,102,108,97,103,45,97,114,111,117,110,100,32,40,120,32,123,105,125,41,32,40,121,32,123,106,125,41,32,40,110,117,109,32,48,41,41,39,41,13,10,13,10,32,32,32,32,32,32,32,32,35,32,80,82,73,78,84,83,32,66,79,65,82,68,32,40,98,101,102,111,114,101,32,101,120,101,99,117,116,105,111,110,41,32,84,79,32,84,69,82,77,73,78,65,76,32,35,35,13,10,32,32,32,32,32,32,32,32,32,32,32,32,105,102,32,40,105,44,106,41,32,110,111,116,32,105,110,32,112,111,115,105,116,105,111,110,115,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,112,114,105,110,116,40,105,110,102,111,91,105,93,91,106,93,44,32,101,110,100,61,34,32,34,41,13,10,32,32,32,32,32,32,32,32,32,32,32,32,101,108,115,101,58,13,10,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,112,114,105,110,116,40,34,88,34,44,32,101,110,100,61,34,32,34,41,13,10,32,32,32,32,32,32,32,32,112,114,105,110,116,40,41,13,10,13,10,32,32,32,32,35,32,83,116,97,114,116,115,32,116,104,101,32,97,103,101,110,116,13,10,32,32,32,32,101,110,118,46,114,117,110,40,41,13,10,13,10,32,32,32,32,35,32,80,82,73,78,84,83,32,66,79,65,82,68,32,40,97,102,116,101,114,32,101,120,101,99,117,116,105,111,110,41,32,84,79,32,84,72,69,32,84,69,82,77,73,78,65,76,32,35,13,10,32,32,32,32,102,32,61,32,101,110,118,46,102,97,99,116,115,40,41,13,10,32,32,32,32,99,117,114,114,101,110,116,95,115,116,97,116,101,40,102,41
>>>>>>> 86ae8622037d08baeee0db9c125f4081a888c7b4
