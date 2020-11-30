'''
reader.py
I/O Module for Minesweeper Board
'''

def read_board():
    ''' Read board inputs from terminal '''
    
    board_size = int(input())
    total_bombs = int(input())

    bombs = []

    for i in range(total_bombs):
        temp = input()
        x,y = map(int, temp.split(', '))
        bombs.append((x,y))

    return board_size, total_bombs, bombs

def read_board_file(filename='input.txt'):
    ''' Read board inputs from a txt file '''
    
    with open(filename, 'r') as f:
        board_size = int(f.readline())
        total_bombs = int(f.readline())
        bombs = []
        for i in range(total_bombs):
            x, y = map(int, f.readline().split(","))
            bombs.append((x, y))
        
        return board_size, total_bombs, bombs

if __name__ == "__main__":
    b, t, m = read_board()
    print(b, t, m)