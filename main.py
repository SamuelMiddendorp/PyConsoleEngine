import curses as cs
import time
import math
import copy
from physicsobjects import *
GRAVITY = 0.1
FRICTION = 0.99
BOUNCE = 0.01
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
        for y in range(round(y1), round(y2)):
            window.addstr(round(y),round(x1), " ", cs.color_pair(1))
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
            for x in range(round(x1), round(x2)):
                window.addstr(round(y),round(x), " ", cs.color_pair(1)) 
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
            for y in range(round(y1), round(y2)):
                window.addstr(round(y),round(x), " ", cs.color_pair(1)) 
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    x += incr
                    bh_threshold += 1
def update_points(points: list):
    for point in points:
        if point.fixed:
            continue
        old_point = copy.copy(point)
        point.x += (point.x - point.old_x) * FRICTION
        point.y += (point.y - point.old_y) * FRICTION
        point.y += GRAVITY
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
        if not link.p1.fixed:
            link.p1.x -= offset_x
            link.p1.y -= offset_y
        if not link.p2.fixed:
            link.p2.x += offset_x
            link.p2.y += offset_y
def constrain_points(points, constraints):
    for p in points:
        if p.fixed:
            continue
        vx = p.x - p.old_x
        vy = p.y - p.old_y
        if p.x > constraints[1]:
            p.x = constraints[1]
            p.old_x = p.x + vx * BOUNCE
        elif p.x < 0:
            p.x = 0
            p.old_x = p.x + vx * BOUNCE
        if p.y > constraints[0]:
            p.y = constraints[0]
            p.old_y = p.y + vy * BOUNCE
        elif p.y < 0:
            p.y = 0
            p.old_y = p.y + vy * BOUNCE
def generate_points(rows, cols, spacing, initial_y_offset = 0, initial_x_offset = 0) -> list:
    points = list()
    for y in range(initial_y_offset, rows + initial_y_offset):
        for x in range(initial_x_offset, cols + initial_x_offset):
            if y == initial_y_offset and (x % 3 == 0):
                points.append(Point(y * spacing, x * spacing, y * spacing, x * spacing, True))
            else:
                points.append(Point(y * spacing, x * spacing, y * spacing, x * spacing))
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
def debug(window, msg):
    window.addstr(1,0,msg)
def main(stdscr):
    constraints = [0,0]
    y,x = stdscr.getmaxyx()
    constraints[0] = y -1
    constraints[1] = x -1
    window = cs.newpad(y,x)
    window.nodelay(1)
    window.keypad(1)
    window.notimeout(1)
    window.idlok(1)
    PHYSICS_CAL_AMOUNT = 1
    cs.noecho()
    cs.cbreak()
    cs.curs_set(0)
    cs.mouseinterval(0)
    cs.mousemask(-1)
    cs.start_color()
    points = [Point(5,5,5,5),
              Point(5,15,5,15), 
              Point(10,5,10,5), 
              Point(10,15,10,15), 
              Point(20,15,20,15), 
              Point(30,5,30,5), 
              Point(30,25,30,25),
              Point(30,10,30,10),
              Point(30,15,30,15)
              ]
    links = [Link(points[0], points[1], get_distance(points[0], points[1])),
             Link(points[1], points[3], get_distance(points[1], points[3])),
             Link(points[0], points[2], get_distance(points[0], points[2])), 
             Link(points[2], points[3], get_distance(points[2], points[3])),  
             Link(points[1], points[2], get_distance(points[1], points[2])),
             Link(points[0], points[3], get_distance(points[2], points[3])),
             Link(points[3], points[4], get_distance(points[3], points[4])),
             Link(points[4], points[5], get_distance(points[4], points[5])),
             Link(points[4], points[6], get_distance(points[4], points[6])),
             Link(points[4], points[7], get_distance(points[4], points[7])),
             Link(points[4], points[8], get_distance(points[4], points[8])),
             Link(points[6], points[8], get_distance(points[6], points[8])),
             Link(points[5], points[7], get_distance(points[5], points[7]))
             ]
    stickfigure = PhysicsBody(points, links)
    # box_points = [Point(5,5,5,5), Point(5,50,5,50), Point(25,5,25,5), Point(25,50,25,50)]
    # box_links = [Link(box_points[0], box_points[1], get_distance(box_points[0], box_points[1])),
    #              Link(box_points[1], box_points[3], get_distance(box_points[1], box_points[3])),
    #              #Link(box_points[1], box_points[2], get_distance(box_points[1], box_points[2])),
    #              Link(box_points[0], box_points[2], get_distance(box_points[0], box_points[2])),
    #              #Link(box_points[0], box_points[3], get_distance(box_points[0], box_points[3])),
    #              Link(box_points[2], box_points[3], get_distance(box_points[2], box_points[3]))]
    box_points = generate_points(10,10,10,1)
    box_links = generate_links(box_points, 10,10)
    fps = 60
    max_p = len(points) - 1
    point_index = 0
    steps = 500
    cs.init_pair(1, cs.COLOR_WHITE, 22)
    cs.init_pair(2, cs.COLOR_WHITE, 55)
    pickup = False
    FRAMES_PER_FPS_DISPLAY = 10
    frame_count = 0 
    mouse_info = None
    current_ms = 0
    while True:
        updateTime = time.time()
        window.erase()
        event = window.getch()
        if event == 27:
            break
        elif event == cs.KEY_MOUSE:
            mouse_info = cs.getmouse()
            if mouse_info[4] == cs.BUTTON1_PRESSED:
                if  not pickup:
                    for index, point in enumerate(box_points):
                        if round(point.x) == mouse_info[1] and round(point.y) == mouse_info[2]:
                            point_index = index
                            debug(window, f"Foo {point_index}")
                            pickup = True
                else:
                    pickup = False
            
        update_points(box_points)
        for _ in range(PHYSICS_CAL_AMOUNT):
            update_links(box_links)
            constrain_points(box_points, constraints)

        for link in box_links:
            draw_line(link.p1, link.p2, window)
        for point in box_points:
            # For some reason the bounds are not always correct, havent found a solution yet
            try:
                window.addstr(round(point.y), round(point.x), " ", cs.color_pair(1))
            except:
                debug(window, f"{point.y},{point.x}")
        
        if pickup:
            mouse_info = cs.getmouse()
            box_points[point_index].x = mouse_info[1]
            box_points[point_index].old_x = mouse_info[1]
            box_points[point_index].y = mouse_info[2]
            box_points[point_index].old_y = mouse_info[2]
        frame_count += 1
        if frame_count >= FRAMES_PER_FPS_DISPLAY:
            current_ms = 1000*(time.time() - updateTime)
            frame_count = 0
        window.addstr(0,0,f"{current_ms} ms")
        window.refresh(0,0,0,0,y-1,x-1)


    cs.endwin()

if __name__ == "__main__":
    cs.wrapper(main)