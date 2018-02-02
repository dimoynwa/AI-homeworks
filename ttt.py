import random

TABLE_SIZE = 3

X_PLACE = -1
EMPTY_SLOT = 0
O_PLACE = 1

FIRST = O_PLACE

def print_table(table):
    print_map = {0 : '_', 1 : 'O', -1 : 'X'}
    def print_row(row):
        for x in row:
            print(print_map[x], end=' ')
        print()
    for row in table:
        print_row(row)

def winner(table):
    for row in table:
        if abs(sum(row)) == len(table):
            return row[0]
    for i in range(len(table)):
        col = [table[j][i] for j in range(len(table))]
        if abs(sum(col)) == len(table):
            return col[0]
    if abs(sum([table[i][i] for i in range(len(table))])) == TABLE_SIZE:
        return table[0][0]
    if abs(sum([table[i][TABLE_SIZE-1-i] for i in range(len(table))])) == TABLE_SIZE:
        return table[0][TABLE_SIZE-1]
    return 0

def all_filled(table):
    for row in table:
        if EMPTY_SLOT in row:
            return False
    return True

def empty_slots(table):
    for row in range(len(table)):
        for col in range(len(table[0])):
            if table[row][col] == EMPTY_SLOT:
                yield (row, col)

def calculate(table, turn, next, alpha, beta):
    win = winner(table)
    if win:
        return win
    if all_filled(table):
        return 0
    for i, j in empty_slots(table):
        table[i][j] = turn
        value = calculate(table, next, turn, alpha, beta)
        table[i][j] = EMPTY_SLOT
        if turn == O_PLACE:
            alpha = max(alpha, value)
            if alpha >= beta:
                return beta
        else:
            beta = min(beta, value)
            if beta <= alpha:
                return alpha
    if turn == X_PLACE:
        return beta
    else:
        return alpha

def computer_move(table):
    best_moves = []
    best_value = -1.1
    for i, j in empty_slots(table):
        table[i][j] = O_PLACE
        new_value = calculate(table, X_PLACE, O_PLACE, -1.1, 1.1)
        table[i][j] = EMPTY_SLOT
        if new_value > best_value:
            best_value = new_value
            best_moves = [(i, j)]
        elif new_value == best_value:
            best_moves.append((i, j))
    row, col = random.choice(best_moves)
    print('Comp choose : ' + str((row + 1,col + 1)))
    table[row][col] = O_PLACE

def human_move(table):
    inp  = input('YOUR TURN : ')
    row, col = (int(x) - 1 for x in inp.split(' '))
    table[row][col] = X_PLACE

def game():
    table = [[EMPTY_SLOT]*TABLE_SIZE for i in range(TABLE_SIZE)]
    next = FIRST
    while not all_filled(table) and not winner(table):
        print_table(table)

        if next == X_PLACE:
            human_move(table)
            next = O_PLACE
        else:
            computer_move(table)
            next = X_PLACE

    final_winner = winner(table)
    if final_winner:
        print_table(table)
        if final_winner == -1:
            print('HUMAN WINS!!!')
        else:
            print('COMPUTER WINS!!!')
    else:
        print('DRAW!!!')


if __name__ == '__main__':
    game()
    
