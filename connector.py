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
                if f['state'] == 'open':
                    g[int(f['x'])][int(f['y'])] = int(f['bombs'])
                else:
                    g[int(f['x'])][int(f['y'])] = -999
        except Exception as e:
            pass
    
    for i in range(size):
        for j in range(size):
            if g[i][j] == -999:
                print('█', end=" ")
            else:
                print(g[i][j], end=" ")
        print()

if __name__ == "__main__":

    env = clips.Environment()
    env.load('C:\\Users\\Hengky\\Desktop\\minesweeper-agent\\minesweeper.clp')
    env.reset()

    size, total, positions = reader.read_board_file('input-mini.txt')

    # Defines the board size and total number of mines
    board_fact = f'(board {size})'
    mines_fact = f'(total_mines {total})'

    env.assert_string(board_fact)
    env.assert_string(mines_fact)

    info = define_tiles(size, positions)
    for i in range(size):
        for j in range(size):
            tiles_fact = f'(tile (x {i}) (y {j}) (bombs {info[i][j]}) (state close))'
            env.assert_string(tiles_fact)

        ## PRINTS BOARD TO TERMINAL ##
        #     if (i,j) not in positions:
        #         print(info[i][j], end=" ")
        #     else:
        #         print("X", end=" ")
        # print()

    env.run()
    for f in env.facts():
        print(f)
    current_state(env.facts())