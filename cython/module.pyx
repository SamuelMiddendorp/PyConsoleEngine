cdef class Point:
    cdef public float x,y,x_old,y_old
    cdef public bint fixed
    def __init__(self, x, y, x_old, y_old, fixed = False):
        self.x = x
        self.y = y
        self.x_old = x_old
        self.y_old = y_old
        self.fixed = fixed
def generate_points(numPoints):
    points = []
    for _ in range(numPoints):
        points.append(Point(2,2,2,2))
    return points
def typed_loop():
    cdef list points = generate_points(100000)
    cdef Point ptn
    cdef float sum_points = 0
    for ptn in points:
        sum_points += ptn.x
    return sum_points



