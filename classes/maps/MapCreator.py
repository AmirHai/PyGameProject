print('название комнат:', end='')
for i in range(25):
    if i % 5 == 0:
        print()
    print(i + 1, end=' ')

fileName = input()

f = open(f'{fileName}.csv', 'w', encoding='utf8')
board = [[0] * 115 for _ in range(115)]

cabinets = input().split()
koridors = input().split(';')
playerCabinet = int(input())

for q in cabinets:
    i1 = (int(q) - 1) // 5
    j1 = (int(q) - 1) % 5
    for i in range((15 + 10) * i1, (15 + 10) * i1 + 15):
        for j in range((15 + 10) * j1, (15 + 10) * j1 + 15):
            if i == (15 + 10) * i1 or i == (15 + 10) * i1 + 14 or j == (15 + 10) * j1 or j == (15 + 10) * j1 + 14:
                board[i][j] = 2
            else:
                if int(q) - 1 == playerCabinet - 1:
                    board[i][j] = 3
                    if i == i1 + 5 and j == j1 + 5:
                        board[i][j] = 4
                else:
                    board[i][j] = 1

for q in koridors:
    kabinets = [int(w) - 1 for w in q.split()]
    if abs(kabinets[0] - kabinets[1]) == 1:
        i1 = kabinets[0] // 5 * (15 + 10) + 4
        j1 = kabinets[0] % 5 * (15 + 10) + 14
        for i in range(i1, i1 + 7):
            for j in range(j1, j1 + 12):
                if i == i1 or i == i1 + 6:
                    board[i][j] = 2
                else:
                    board[i][j] = 3
    else:
        i1 = kabinets[0] // 5 * (15 + 10) + 14
        j1 = kabinets[0] % 5 * (15 + 10) + 4
        for i in range(i1, i1 + 12):
            for j in range(j1, j1 + 7):
                if j == j1 or j == j1 + 6:
                    board[i][j] = 2
                else:
                    board[i][j] = 3


for i in range(115):
    stroke = ' '.join([str(j) for j in board[i]])
    if i != 114:
        f.write(f'{stroke}\n')
    else:
        f.write(f'{stroke}')
