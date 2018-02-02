import math
import random
from PIL import Image

FILE_NAMES = ['normal.txt', 'unbalance.txt']
COLORS = [(0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 0, 0),
          (128, 128, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128) ]

HEIGTH = 200
WEIGTH = 200

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

class Cluster:
    def __init__(self, num, center, points=[]):
        self.num = num
        self.points = points
        self.center = center

    def add_point(self, p):
        self.points.append(p)

    def clear(self):
        self.points = []

def print_cluster(cluster):
    print('Cluster ' + str(cluster.num))
    print('Center : ' + str(cluster.center))
    print('Number of points : ' + str(len(cluster.points)))
    #for p in cluster.points:
        #print(p)
    print('\n\n\n')

def distance(p1, p2):
    return math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y,2))

def load_points(file_name):
    spl = {FILE_NAMES[0] : '\t', FILE_NAMES[1] : ' '}
    points = []
    MAX_X, MAX_Y, MIN_X, MIN_Y = 0, 0, 999999, 999999
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            p = line.split(spl[file_name])
            x, y = float(p[0]), float(p[1])
            if x > MAX_X:
                MAX_X = x
            if y > MAX_Y:
                MAX_Y = y
            if x < MIN_X:
                MIN_X = x
            if y < MIN_Y:
                MIN_Y = y
            points.append(Point(x, y))
    return points, MAX_X, MAX_Y, MIN_X, MIN_Y

def random_point(max_x, max_y):
    x, y = random.uniform(0.0, max_x), random.uniform(0.0, max_y)
    return Point(x, y)

def allocate(clusters, points):
    for point in points:
        min_dist = distance(point, clusters[0].center)
        cluster = clusters[0]
        for i in range(1, len(clusters)):
            dist = distance(point, clusters[i].center)
            if dist < min_dist:
                min_dist = dist
                cluster = clusters[i]
        cluster.add_point(point)

def change_center(cluster):
    if not len(cluster.points):
        return
    #print('Old center : ' + str(cluster.center))
    sum_x, sum_y = 0, 0
    for p in cluster.points:
        sum_x += p.x
        sum_y += p.y
    #print('SUM   X : ' + str(sum_x) + '    Y : ' + str(sum_y) + '   len : ' + str(len(cluster.points)))
    cluster.center = Point(sum_x / (float)(len(cluster.points)),
                           sum_y / (float)(len(cluster.points)))

def transform(x, coord, MIN, MAX):
    coef = (x-MIN)/(MAX-MIN)
    if coef == 1:
        coef = 0.099999
    return coord*coef

def create_image(file_name, clusters, MIN_X, MIN_Y, MAX_X, MAX_Y):
    w = WEIGTH
    h = HEIGTH
    #print('Size : ' + str((int(w), int(h))))
    im = Image.new('RGB', (int(w), int(h)), 'white')
    pixels = im.load()
    for cluster in clusters:
        for point in cluster.points:
            x = transform(point.x, w, MAX_X, MIN_X) 
            y = transform(point.y, h, MAX_Y, MIN_Y)
            #print('x : ' + str(x) + '   y : ' + str(y))
            pixels[int(x), int(y)] = (0, 0, 0)
        #print('-----' +str(cluster.center.x) + '   ' + str(MAX_X) + '    '+ str(MIN_X))
        #print('-----' +str(cluster.center.y) + '   ' + str(MAX_Y) + '    '+ str(MIN_Y))
        c_x = transform(cluster.center.x, w, MAX_X, MIN_X)
        c_y = transform(cluster.center.y, h, MAX_Y, MIN_Y)
        #print(str(c_x) + '    ' + str(c_y))
        pixels[int(c_x), int(c_y)] = (255, 0, 0)
    im.save(file_name)
    im.show()

def k_means(file_name, k):
    points, MAX_X, MAX_Y, MIN_X, MIN_Y = load_points(file_name)
    clusters = []
    for i in range(k):
        clusters.append(Cluster(i, random_point(MAX_X, MAX_Y)))
    is_finish = False
    iteration = 0
    while not is_finish:
        #print('Iteration : ' + str(iteration))
        for cluster in clusters:
            cluster.clear()
        old_centers = [Point(clusters[i].center.x, clusters[i].center.y)
                           for i in range(len(clusters))]
        allocate(clusters, points)

        for cluster in clusters:
            change_center(cluster)

        diff = sum([distance(old_centers[i], clusters[i].center)
                    for i in range(len(clusters))])
        is_finish = diff == 0
    for cluster in clusters:
        print_cluster(cluster)
    #Create Image
    create_image(file_name[0: len(file_name) - 4] + '.png', clusters,
                     MIN_X, MIN_Y, MAX_X, MAX_Y)
    
if __name__ == '__main__':
    s = input()
    s = s.split(' ')
    k_means(s[0], int(s[1]))






        
