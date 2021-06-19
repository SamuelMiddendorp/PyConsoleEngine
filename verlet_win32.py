import win32console, win32con, time, win32api
import copy
import math
import random
from physicsobjects import *
GRAVITY = 0.1
FRICTION = 0.99
BOUNCE = 0.01

dims = (400,120)
def get_distance(p1, p2): 
    dx = p2.x - p1.x
    dy = p2.y -p1.y
    return math.sqrt(dx * dx + dy * dy)
def draw_line(p1: Point, p2: Point, world: list):
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
            world[y * dims[0] + round(x1)] = "\u2588"
            #window.addstr(round(y),round(x1), " ", cs.color_pair(1))
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
                #window.addstr(round(y),round(x), " ", cs.color_pair(1)) 
                world[round(y) * dims[0] + x] = "\u2588"
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
                world[y * dims[0] + round(x)] = "\u2588"
                #window.addstr(round(y),round(x), " ", cs.color_pair(1)) 
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    x += incr
                    bh_threshold += 1
def update_points(points: list):
    for point in points:
        if not point.fixed:
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
def constrain_points(points, world, constraints):
    for p in points:
        if p.fixed:
            continue
        vx = p.x - p.old_x
        vy = p.y - p.old_y
        if p.x > constraints[0]:
            p.x = constraints[0]
            p.old_x = p.x + vx * BOUNCE
        elif p.x < 0:
            p.x = 0
            p.old_x = p.x + vx * BOUNCE
        if p.y > constraints[1]:
            p.y = constraints[1]
            p.old_y = p.y + vy * BOUNCE
        elif p.y < 0:
            p.y = 0
            p.old_y = p.y + vy * BOUNCE
        world[round(p.y) * dims[0] + round(p.x)] = "\u2588"
def generate_points(rows, cols, spacing, initial_y_offset = 0, initial_x_offset = 0) -> list:
    points = list()
    for y in range(initial_y_offset, rows + initial_y_offset):
        for x in range(initial_x_offset, cols + initial_x_offset):
            if y == initial_y_offset and (x % 3 == 0 or x == cols + initial_x_offset -1):
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
def setup_screen(dims: tuple):
    myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                                       ShareMode=0,
                                                       SecurityAttributes=None,
                                                       Flags=1)
    myConsole.SetConsoleWindowInfo(Absolute=True,ConsoleWindow = win32console.PySMALL_RECTType(0,0,1,1))                                               
    myConsole.SetConsoleScreenBufferSize(win32console.PyCOORDType(dims[0],dims[1]))
    myConsole.SetConsoleWindowInfo(Absolute=True,ConsoleWindow = win32console.PySMALL_RECTType(0,0,dims[0]-1,dims[1]-1))  
    #myConsole.SetConsoleDisplayMode(Flags=win32console.CONSOLE_FULLSCREEN, NewScreenBufferDimensions = win32console.PyCOORDType(200,50))                                      
    myConsole.SetConsoleActiveScreenBuffer()
    myConsole.SetConsoleCursorInfo(Size=1,Visible=0)
    return myConsole
def setup_empty_world(total_size):
    world = []
    for x in range(total_size):
        world.append(" ")
    return world
def clear_world(world, size):
    for x in range(len(world)):
        world[x] = " "
def main():
    total_size = dims[0] * dims[1]
    console = setup_screen(dims)
    cloth_points = generate_points(8,24,10)
    cloth_links = generate_links(cloth_points,8,24)
    world = setup_empty_world(total_size)
    force_timer = 0
    fps = 30
    amount_cloth_points = len(cloth_points)
    force_interval = 4000
    while True: 
        begin_time = time.time()
        clear_world(world,total_size)
        update_points(cloth_points)
        update_links(cloth_links)
        constrain_points(cloth_points, world, (dims[0] - 1, dims[1] -1)) 
        if force_timer > force_interval:
            cloth_points[amount_cloth_points-1].x += 50
            cloth_points[amount_cloth_points-1].old_x += 50
            force_timer = 0
        for link in cloth_links:
            draw_line(link.p1, link.p2, world)
        console.WriteConsoleOutputCharacter("".join(world),win32console.PyCOORDType(0, 0))
        ms = 1000 * (time.time() - begin_time)
        force_timer += ms + 1000/fps
        win32console.SetConsoleTitle(f"{ms} ms")
        time.sleep(1/fps - ms/1000)
        #win32console.SetConsoleTitle(f"{win32api.GetCursorPos()} ms")
    
if __name__ == "__main__":
    main()