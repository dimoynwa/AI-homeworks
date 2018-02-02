from queue import PriorityQueue
import random

STARTING_ELEMENTS = 50
GENERATIONS = 25
SAVED_ELEMENTS = 10
GENERATING_PAIRS = 50

COST = []
WEIGTH = []


class Element:
    def __init__(self, elements):
        self.elements = elements

    def __getitem__(self, x):
        return self.elements[x]

    def __setitem__(self, x, y):
        self.elements[x] = y

    def __cmp__(self, other):
        return cmp(self.fitness_func(), other.fitness_func())

    def __lt__(self, other):
        return self.fitness_func() > other.fitness_func()

    def __str__(self):
        return str(self.fitness_func())

    def fitness_func(self):
        return sum([self[i]*COST[i] for i in range(self.length())])

    def length(self):
        return len(self.elements)
    
    def weigth(self):
        return sum([self[i]*WEIGTH[i] for i in range(self.length())])

    def validate(self, m):
        while self.weigth() > m:
            i = random.choice([i for i in range(self.length()) if self[i] == 1])
            self[i] = 0

    def mutate(self, m):
        ind = random.randint(0, self.length() - 1)
        if not self[ind]:
            self[ind] = 1
            if self.weigth() > m:
                self[ind] = 0
        else:
            self[ind] = 0


def random_element(n, m):
    elements = []
    for i in range(n):
        elements.append(random.choice([0, 1]))
    el = Element(elements)
    el.validate(m)
    return el

def get_child(el1, el2, m):
    elements = []
    for i in range(el1.length()):
        elements.append(el1[i] ^ el2[i])
    el = Element(elements)
    el.validate(m)
    return el

def new_generation(old, m):
    new = PriorityQueue()
    old_elems = []
    while not old.empty():
        old_elems.append(old.get())
    for i in range(SAVED_ELEMENTS):
        new.put(old_elems[i])
    for i in range(GENERATING_PAIRS):
        el = get_child(old_elems[random.randint(0, len(old_elems) - 1)],
                       old_elems[random.randint(0, len(old_elems) - 1)], m)
        el.mutate(m)
        new.put(el)
    return new

def main():
    #m = int(input("Max weigth : "))
    #n = int(input("Number of objects : "))
    s = input().split(' ')
    m, n = int(s[0]), int(s[1])
    for i in range(n):
        s = input()
        ns = s.split(' ')
        COST.append(int(ns[0]))
        WEIGTH.append(int(ns[1]))

    #print('COST : ' + str(COST))
    #print('WEIGTH : ' + str(WEIGTH))
    
    q = PriorityQueue()
    for i in range(STARTING_ELEMENTS):
        q.put(random_element(n, m))
    for i in range(GENERATIONS):
        q = new_generation(q, m)
    return q.get()
    
if __name__ == '__main__' :
    res = main()
    #print(str(res.elements))
    print(res)
