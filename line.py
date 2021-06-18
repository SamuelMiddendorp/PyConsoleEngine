p1 = [4,15]
p2 = [9,18]
def get_points(p1, p2):
    points = list()
    x1 = p1[1]
    x2 = p2[1]
    y1 = p1[0]
    y2 = p2[0]
    dy = y2 - y1
    dx = x2 - x1
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
points = get_points(p1,p2)
for y in range(10):
    newLine = ""
    for x in range(20):
        if((x == p1[1] and y == p1[0]) or (x == p2[1] and y == p2[0])):
            newLine += "p"
            continue
        hasPoint = False
        for point in points:
            if(x == point[1] and y == point[0]):
                newLine += "-"
                hasPoint = True
        if not hasPoint:
            newLine += "."
    print(newLine + "\n")
