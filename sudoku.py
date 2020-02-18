def newBoard():
    return [[0 for y in range(9)] for x in range(9)]


def validate(board, index, num):
    x, y = index
    for z in range(9):
        if num == board[z][x] or num == board[y][z]:
            return False
    const_x = (x // 3) * 3
    const_y = (y // 3) * 3
    for z in range(3):
        for a in range(3):
            if num == board[z + const_y][a + const_x]:
                return False
    return True


def findEmptySpace(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return x, y


def solve(board):
    if not findEmptySpace(board):
        return True
    index = findEmptySpace(board)
    for num in range(1, 10):
        if validate(board, index, num):
            x, y = index
            board[y][x] = num
            if solve(board):
                return True
            board[y][x] = 0
