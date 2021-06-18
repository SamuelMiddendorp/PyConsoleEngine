import curses as cs
import time
import  math
import copy
from physicsobjects import *
def get_distance(p1, p2): 
    dx = p2.x - p1.x
    dy = p2.y -p1.y
    return math.sqrt(dx * dx + dy * dy)
def draw_line(p1: Point, p2: Point, window):
    points = list()
    x1 = p1.x
    x2 = p2.x
    y1 = p1.y
    y2 = p2.y
    dy = y2 - y1
    dx = x2 - x1
    if dx == 0:
        if y2 < y1:
            y1 = p2.y
            y2 = p1.y
        for y in range(y1, y2):
            window.addstr(y,x1, " ",cs.color_pair(1))
    # elif dy == 0:
    #     if x2 > x1:
    #         x1 = p2.x
    #         x2 = p1.x
    #     for x in range(x1, x2 + 1):
    #         window.addstr(y,x1, " ",cs.color_pair(1))
    # if dy == 0:
    #     if x2 > x1:
    #         x1 = p2.x
    #         x2 = p1.x
    #     for x in range(x1, x2+1):
    #         window.addstr(y1,x, " ",cs.color_pair(1))
    else:
        coef = dy / dx
        bh_offset = 0
        incr = 1 if coef >= 0 else -1
        bh_threshold = 0.5
        if coef <= 1 and coef >= -1:
            y = y1
            delt = abs(coef)
            if x2 < x1:
                x1 = p2.x
                x2 = p1.x
                y = y2
            for x in range(x1, x2):
                try:
                    window.addstr(y,x, " ",cs.color_pair(1)) 
                except:
                    pass
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    y += incr
                    bh_threshold += 1
        else:
            x = x1
            delt = abs(dx/dy)
            if y2 < y1:
                y1 = p2.y
                y2 = p1.y
                x = x2
            for y in range(y1, y2):
                try:
                    window.addstr(y,x, " ",cs.color_pair(1)) 
                except:
                    pass
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    x += incr
                    bh_threshold += 1
def update_points(points: list):
    for point in points:
        old_point = copy.copy(point)
        point.x += point.x - point.old_x
        point.y += point.y - point.old_y
        point.old_x = old_point.x
        point.old_y = old_point.y
def update_links(links: list):
    for link in links:
        dx = link.p2.x - link.p1.x
        dy = link.p2.y - link.p1.y
        dist = math.sqrt(dx * dx + dy * dy)
        diff = link.len - dist
        try:
            percent = diff / dist / 2
        except:
            percent = 0
        offset_x = dx * percent
        offset_y = dy * percent
        link.p1.x -= round(offset_x)
        link.p1.y -= round(offset_y)
        link.p2.x += round(offset_x)
        link.p2.y += round(offset_y)
def constrain_points(points, constraints):
            # up and bottom bounds
    for p in points:
        vx = p.x - p.old_x
        vy = p.y - p.old_y
        if p.x > constraints[1]:
            p.x = constraints[1]
            p.old_x = p.x + vx
        elif p.x < 0:
            p.x = 0
            p.old_x = p.x + vx
        #right and left bounds
        if p.y > constraints[0]:
            p.y = constraints[0]
            p.old_y = p.y + vy
        elif p.y < 0:
            p.y = 0
            p.old_y = p.y + vy
def generate_points(rows, cols, spacing, initial_y_offset = 0, initial_x_offset = 0) -> list:
    points = list()
    for y in range(initial_y_offset, rows + initial_y_offset):
        for x in range(initial_x_offset, cols + initial_x_offset):
            points.append(Point(y * spacing, x * spacing, y * spacing, x * spacing))
    points[len(points)-1].x += 1
    return points
def generate_links(points, rows, cols, spacing):
    links = list()
    for y in range(rows):
        for x in range(cols):
            try:
                links.append(Link(points[y * rows + x], points[(y + 1) * rows + x], spacing))
            except:
                pass
            try:
                links.append(Link(points[y * rows + x], points[y * rows + x + 1], spacing))
            except:
                pass

    return links
def main():
    # Clear screen
    cs.initscr()
    last_time = time.time()
    counter = 0
    constraints = [35,100]

    window = cs.newpad(constraints[0] + 1, constraints[1] + 1)
    window.border(0)
    window.nodelay(1)
    cs.noecho()
    cs.curs_set(0)
    cs.start_color()
    #points = [Point(5,3,3,3), Point(3,3,3,6), Point(3,3,10,6), Point(1,1,1,1)]
    #points = generate_points(10,10,3,1,1)
    #links = generate_links(points,10,10,5)
    points = [Point(5,5,5,5), Point(5,15,5,15), Point(10,5,10,5), Point(10,15,10,15), Point(20,15,20,15), Point(30,5,30,5), Point(30,25,30,25)]
    links = [Link(points[0], points[1], 10),
            Link(points[1], points[3], 5),
            Link(points[0], points[2], 5), 
            Link(points[2], points[3], 10), 
            Link(points[0], points[3], 12), 
            Link(points[1], points[2], 10),
            Link(points[3], points[4], 10),
            Link(points[4], points[5], 15),
            Link(points[4], points[6], 15),]
    #links = [Link(points[0], points[1], 10), Link(points[1], points[2], 10),Link(points[2], points[0], 10), Link(points[3], points[0], 10), Link(points[3], points[2], 10)]
    fps = 60
    steps = 500
        #render
    cs.init_pair(1, cs.COLOR_WHITE, 22)
    colorCount = 0
    while True:
        updateTime = time.time()
        # This raises ZeroDivisionError when i == 10. 
        event = window.getch()
        if event == 27:
            break
        elif event == 122:
            points[6].x += 1
        window.erase()
        #calculate
        update_points(points)
        # multiple passes of link adjusting
        update_links(links)
        constrain_points(points, constraints)
        #line
        #cs.init_pair(1, cs.COLOR_WHITE, colorCount)
        # if colorCount >= 255:
        #     colorCount = 0
        # colorCount += 1
        #render
        for link in links:
            draw_line(link.p1, link.p2, window)
        for point in points:
            try:
                window.addstr(point.y, point.x, "p", cs.color_pair(1))
            except:
                pass
        window.addstr(0,0,f"{(time.time() - updateTime)} ms")
        window.refresh( 0,0, 0,0, constraints[0] + 1,constraints[1] + 1)
        time.sleep(1/fps)

    cs.endwin()

if __name__ == "__main__":
    #cs.wrapper(main)
    main()