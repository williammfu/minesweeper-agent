'''
File: connector.py

The following file initiates
a minesweeper board inside the CLIPS environment
'''

import clips # clipspy
import reader
import itertools
import sys

from gui import Board


CLOSED = -999
FLAGGED = -1

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
                
                if f['state'] == 'open':
                    g[int(f['x'])][int(f['y'])] = int(f['bombs'])
                elif f['state'] == 'close':
                    g[int(f['x'])][int(f['y'])] = CLOSED
                elif f['state'] == 'flagged':
                    g[int(f['x'])][int(f['y'])] = FLAGGED
  
        except Exception as e:
            pass
    
    # Menampilkan hasil operasi agen minesweeper pada layar
    for i in range(size):
        for j in range(size):
            if g[i][j] == CLOSED:
                print('█', end=" ")
            elif g[i][j] == FLAGGED:
                print('F', end=" ")
            else:
                print(g[i][j], end=" ")
        print()


def find_tile_facts(b_size, facts):
    ''' Defines board state by
    looking at the Working Memory Facts '''

    g = [[0 for i in range(b_size)] for j in range(b_size)]

    for f in facts:
        try:
            if f['x'] >= 0:
                
                if f['state'] == 'open':
                    g[int(f['x'])][int(f['y'])] = int(f['bombs'])
                elif f['state'] == 'close':
                    g[int(f['x'])][int(f['y'])] = CLOSED
                elif f['state'] == 'flagged':
                    g[int(f['x'])][int(f['y'])] = FLAGGED
            
        except Exception as e:
            pass
    
    return g


if __name__ == "__main__":

    # Setup environment CLIPS 
    env = clips.Environment()
    env.load('minesweeper.clp')
    env.reset()
    
    size, total, positions = 0, 0, []

    if len(sys.argv) < 2:
        size, total, positions = reader.read_board()
    else:
        size, total, positions = reader.read_board_file(sys.argv[1])

    # Defines the board size and total number of mines
    board_fact = f'(board (size {size}) (total-mines {total}))'

    # Asserts board size and total-mines to the env
    env.assert_string(board_fact)

    # Assigns each tiles with the corresponding value based on
    # the number of bombs
    info = define_tiles(size, positions)
    board = Board(info)
    board.mainloop()

    for i in range(size):
        for j in range(size):
            tiles_fact = f'(tile (x {i}) (y {j}) (bombs {info[i][j]}) (state close))'
            env.assert_string(tiles_fact)
            env.assert_string(f'(flag-around (x {i}) (y {j}) (num 0))')

        # PRINTS BOARD (before execution) TO TERMINAL ##
            if (i,j) not in positions:
                print(info[i][j], end=" ")
            else:
                print("X", end=" ")
        print()

    # Starts the agent
    env.run()

    # PRINTS BOARD (after execution) TO THE TERMINAL #
    f = env.facts()
    current_state(f)