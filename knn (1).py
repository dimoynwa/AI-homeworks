from random import shuffle
import math
from queue import PriorityQueue
import operator

DATA_SIZE = 4
TEST_SET_SIZE = 20
FILE_NAME = 'iris.txt'

class Elem:
    def __init__(self, data, cls):
        self.data = data
        self.cls = cls

def load_elements(file_path):
    elements = []
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            spl = line.split(',')
            data = [float(spl[i]) for i in range(DATA_SIZE)]
            cls = spl[-1]
            elements.append(Elem(data, cls))
    return elements

def make_sets(elements):
    shuffle(elements)
    test_set = elements[0:TEST_SET_SIZE]
    training_set = elements[TEST_SET_SIZE: len(elements)]
    return (test_set, training_set)

def dist(elem1, elem2):
    distance = 0
    for i in range(DATA_SIZE):
        distance += pow((elem1.data[i] - elem2.data[i]), 2)
    return math.sqrt(distance)

def neighbors(inst, training_set, k):
    queue = []
    neigh = []
    distance = 0
    for x in training_set:
        distance = dist(inst, x)
        c = distance, x
        #print('C : ' + str(c))
        queue.append(c)
    queue.sort(key=operator.itemgetter(0))
    #print('Queue : ' + str(queue))
    for i in range(k):
        neigh.append(queue[i][1])
    #print('Neighbours : ' + str(neigh))
    return neigh

def predict(neigh):
    votes = dict()
    for x in neigh:
        if x.cls in votes:
            votes[x.cls] += 1
        else:
            votes[x.cls] = 1
    predict_class = ''
    predict_votes = 0
    for key in votes:
        if votes[key] > predict_votes:
            predict_votes = votes[key]
            predict_class = key
    #print('Predict votes : ' + str(predict_votes))
    #print('Predict class : ' + str(predict_class))
    return predict_class

def accuracy(test_set, predictions):
    correct = 0
    for x in range(len(test_set)):
        if test_set[x].cls == predictions[x]:
            correct += 1
    return (correct/float(len(test_set))) * 100.0

def knn(k):
    elements = load_elements(FILE_NAME)
    test_set, training_set = make_sets(elements)
    predictions = []
    for test in test_set:
        n = neighbors(test, training_set, k)
        pr = predict(n)
        predictions.append(pr)
        print('predicted=' + str(pr) + ', actual=' + str(test.cls) + '\n')
    ac = accuracy(test_set, predictions)
    print('Accuracy : ' + str(ac) + ' %')

if __name__ == '__main__':
    number = input()
    k = int(number)
    knn(k)
