import time
import os
def get_points(p1, p2):
    points = list()
    x1 = p1[1]
    x2 = p2[1]
    y1 = p1[0]
    y2 = p2[0]
    dy = y2 - y1
    dx = x2 - x1
    if dx == 0:
        if y2 > y1:
            y1 = p2[0]
            y2 = p1[0]
        for y in range(y1, y2 + 1):
            points.append([y,x1])
    else:
        coef = dy / dx
        bh_offset = 0
        incr = 1 if coef >= 0 else -1
        bh_threshold = 0.5
        if coef <= 1 and coef >= -1:
            y = y1
            delt = abs(coef)
            if x2 < x1:
                x1 = p2[1]
                x2 = p1[1]
                y = y2
            for x in range(x1, x2 + 1):
                points.append([y,x])
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    y += incr
                    bh_threshold += 1
        else:
            x = x1
            delt = abs(dx/dy)
            if y2 < y1:
                y1 = p2[0]
                y2 = p1[0]
                x = x2
            for y in range(y1, y2 + 1):
                points.append([y,x])
                bh_offset += delt
                if bh_offset >= bh_threshold:
                    x += incr
                    bh_threshold += 1
    return points
def main():
    os.system('cls')
    constraints = [20,20]
    balls = [[[11,6],[10,5]],[[2,3],[2,3]]]
    line = get_points(balls[0][1], balls[1][1])
    fps = 5
    steps = 500
        #render
    for _ in range(steps):
        #calculate
        for ball in balls:
            old_ball = list.copy(ball[1])
            ball[1][0] += ball[1][0] - ball[0][0]
            ball[1][1] += ball[1][1] - ball[0][1]
            ball[0] = old_ball
            # up and bottom bounds
            if ball[1][0] >= constraints[0]:
                ball[1][0] -= 1
                ball[0][0] = constraints[0]
            elif ball[1][0] <= 0:
                ball[1][0] = 0
                ball[0][0] = -1 
            #right and left bounds
            if ball[1][1] >= constraints[1]:
                ball[1][1] -= 1
                ball[0][1] = constraints[1]
            elif ball[1][1] <= 0:
                ball[1][1] = 0
                ball[0][1] = -1 
        #line
        line = get_points(balls[0][1], balls[1][1])
        #render
        for y in range(constraints[0]):
            row = ""
            for x in range(constraints[1]):
                needsChar = True
                for ball in balls:
                    if(y == round(ball[1][0]) and x == round(ball[1][1])):
                        row += "#"
                        needsChar = False
                        break
                for point in line:
                    if(needsChar and y == point[0] and x == point[1]):
                        row += "-"
                        needsChar = False
                        break
                if needsChar:
                    row += "."
            print(row + "\n")   
        time.sleep(1/fps)
        os.system('cls')
if __name__ == "__main__":
    main()