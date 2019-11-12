def new_board():
    return [[0 for y in range(9)] for x in range(9)]


def validate(board, index, num):
    x, y = index
    for z in range(9):
        if num == board[z][x] or num == board[y][z]:
            return False
    const_x = x // 3
    const_y = y // 3
    for z in range(3):
        for a in range(3):
            if num == board[z + 3 * const_y][a + 3 * const_x]:
                return False
    return True


def find_empty_space(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return x, y


def solve(board):
    if not find_empty_space(board):
        return True
    index = find_empty_space(board)
    for num in range(1, 10):
        if validate(board, index, num):
            x, y = index
            board[y][x] = num
            if solve(board):
                return True
            board[y][x] = 0
