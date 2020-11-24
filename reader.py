'''
reader.py
I/O Module for Minesweeper Board
'''

def board_io():
    ''' Read board inputs from terminal '''
    board_length = int(input())

    n = int(input())

    positions = []

    for i in range(n):
        temp = input()
        value = temp.split(', ')
        positions.append(int(value))

    print(positions)

def read_board_file(filename='input.txt'):
    ''' Read board inputs from a txt file '''
    
    with open(filename, 'r') as f:
        board_size = int(f.readline())
        total_mines = int(f.readline())
        mines = []
        for i in range(total_mines):
            x, y = map(int, f.readline().split(","))
            mines.append((x, y))
        
        return board_size, total_mines, mines

if __name__ == "__main__":
    read_board_file()