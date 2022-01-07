f = open('testMap.csv', 'w', encoding='utf8')
board = [[0] * 100 for _ in range(100)]

for i in range(15):
    for j in range(15):
        if i == 0 or i == 14 or j == 0 or j == 14:
            board[i][j] = 2
        else:
            board[i][j] = 3

for i in range(14, 27):
    for j in range(4, 11):
        if j == 4 or j == 10:
            board[i][j] = 2
        else:
            board[i][j] = 3

for i in range(25, 40):
    for j in range(15):
        if i == 25 or i == 39 or j == 0 or j == 14:
            board[i][j] = 2
        else:
            board[i][j] = 1

for i in range(29, 36):
    for j in range(14, 27):
        if i == 29 or i == 35:
            board[i][j] = 2
        else:
            board[i][j] = 1

for i in range(25, 40):
    for j in range(25, 40):
        if i == 25 or i == 39 or j == 25 or j == 39:
            board[i][j] = 2
        else:
            board[i][j] = 1

for i in range(100):
    stroke = ' '.join([str(j) for j in board[i]])
    f.write(f'{stroke}\n')
