'''
File: connector.py

The following file initiates
a minesweeper board inside the CLIPS environment
'''

import clips # PyClips
import reader
import itertools

env = clips.Environment()
env.load('minesweeper.clp')

# Sets the tiles number 
def define_tiles(size, positions):
    
    tiles = set(range(size))
    radius = set(range(-1,2)) # {-1, 0, 1}
    
    # Minesweeper board representation
    tile_info = [[0 for i in range(size)] for j in range(size)]
    
    for i,j in itertools.product(tiles, tiles):
        bombs = 0
        for m, n in itertools.product(radius, radius):
            if (m,n) == (0,0) or (i+m not in tiles) or (j+n not in tiles):
                continue
            elif (i+m, j+n) in positions:
                bombs += 1

        tile_info[i][j] = bombs # Assign coordinates with number of bombs
    
    return tile_info


if __name__ == "__main__":

    size, total, positions = reader.read_board_file()

    # Defines the board size and total number of mines
    board_fact = f'(board {size})'
    mines_fact = f'(total-mines {total})'

    env.assert_string(board_fact)
    env.assert_string(mines_fact)

    info = define_tiles(size, positions)
    for i in range(10):
        for j in range(10):
            tiles_fact = f'(tile {i} {j} {info[i][j]} close)'
            env.assert_string(tiles_fact)
        
        ## PRINTS BOARD TO TERMINAL ##
        #     if (i,j) not in positions:
        #         print(info[i][j], end=" ")
        #     else:
        #         print("X", end=" ")
        # print()

    env.run()