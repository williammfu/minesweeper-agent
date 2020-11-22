board_length = int(input())

n = int(input())

positions = []

for i in range(n):
    temp = input()
    value = temp.split(', ')
    positions.append(int(value))

print(positions)
