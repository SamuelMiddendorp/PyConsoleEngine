import module
import time
class PyPoint():
    def __init__(self, x, y, x_old, y_old):
        self.x = x
        self.y = y
        self.x_old = x_old
        self.y_old = y_old
def generate_points(numPoints):
    points = []
    for _ in range(numPoints):
        points.append(PyPoint(2,2,2,2))
    return points
def normal_loop():
    points = generate_points(100000)
    sum_points = 0
    for ptn in points:
        sum_points += ptn.x
    return sum_points
def main():
    start = time.time()
    for x in range(10):
        points = normal_loop()
    print(f"{1000 * (time.time() - start)}")
    start = time.time()
    for x in range(10):
        points = module.typed_loop()
    print(f"{1000 * (time.time() - start)}")
if __name__ == "__main__":
    main()