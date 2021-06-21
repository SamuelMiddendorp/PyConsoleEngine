from physicsobjects import *
from numba import jit
import time
import math

def get_distance(p1, p2): 
    dx = p2.x - p1.x
    dy = p2.y -p1.y
    return math.sqrt(dx * dx + dy * dy)
#
@jit
def generate_points(rows, cols, spacing, initial_y_offset = 0, initial_x_offset = 0) -> list:
    points = [[(0, 0, 0) for j in range(rows)] for i in range(cols)]
    for y in range(initial_y_offset, rows + initial_y_offset):
        for x in range(initial_x_offset, cols + initial_x_offset):
            if y == initial_y_offset and (x % 3 == 0 or x == cols + initial_x_offset -1):
                points[x][y] = [x*spacing, x*spacing, y*spacing,y*spacing]
            else:
                points[x][y]= [x*spacing, x*spacing, y*spacing,y*spacing]
    return points
def generate_links(points, rows, cols):
    links = list()
    for y in range(rows):
        for x in range(cols):
            if y != rows -1:
                links.append(Link(points[cols * y + x], points[cols * (y + 1) + x], get_distance(points[cols * y + x], points[cols * (y + 1) + x])))
            if x != cols -1:
                links.append(Link(points[cols * y + x], points[cols * y + x + 1], get_distance(points[cols * y + x], points[cols * y + x + 1])))
    return links
def main():

    generate_points(0,0,2)
    start = time.time()
    for x in range(10):
        points = generate_points(200,200,2)
    print(f"10 iterations took {1000 * (time.time() - start)} ms")
if __name__ == "__main__":
    main()