import random

def min_conflicts(table, iters=10000):
    def random_pos(l, f):
        return random.choice([i for i in range(len(table)) if f(l[i])])
    for k in range(iters):
        confs = find_conflicts(table)
        if sum(confs) == 0:
            return table
        col = random_pos(confs, lambda elt: elt > 0)
        vconfs = [conflict(table, col, row) for row in range(len(table))]
        table[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))
    raise Exception("Incomplete solution: try more iterations.")

def find_conflicts(table):
    return [conflict(table, col, table[col]) for col in range(len(table))]

def conflict(table, col, row):
    total = 0
    for i in range(len(table)):
        if i == col:
            continue
        if table[i] == row or abs(i - col) == abs(table[i] - row):
            total += 1
    return total

def print_tbl(table):
    for i in range(len(table)):
        row = ['_'] * len(table)
        for col in range(len(table)):
            if table[col] == len(table) - 1 - i:
                row[col] = '*'
        print(''.join(row))

def random_start(n):
    start = list(range(n))
    random.shuffle(start)
    return start

def nqueens(n):
    return min_conflicts(random_start(n))

if __name__ == '__main__':
    number = input()
    print_tbl(nqueens(int(number)))
