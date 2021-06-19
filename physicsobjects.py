class Point:
    def __init__(self, old_y, old_x, y,x, fixed = False):
        self.old_y = old_y
        self.old_x = old_x
        self.y = y
        self.x = x
        self.fixed = fixed
class Link:
    def __init__(self, p1, p2, len):
        self.p1 = p1
        self.p2 = p2
        self.len = len
class PhysicsBody:
    def __init__(self, points, links):
        self.points = points
        self.links = links
    

