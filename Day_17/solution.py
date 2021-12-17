def solve(targetArea):
    (x0, x1), (y0, y1) = targetArea
    xMin, xMax = int(-0.5 + (2 * x0) ** 0.5), x1
    yMin, yMax = min(y0, y1), max(abs(y0), abs(y1))
    hitCount, highest = 0, 0
    for u in range(xMin, x1 + 1):
        for v in range(yMin, yMax + 1):
            vx, vy = u, v
            x, y = 0, 0
            highPoint = 0
            while y >= yMin and x <= xMax:
                x += vx
                y += vy
                highPoint = max(highPoint, y)
                vx = max(0, vx - 1)
                vy -= 1
                if x0 <= x <= x1 and y0 <= y <= y1:
                    highest = max(highest, highPoint)
                    hitCount += 1
                    break
    return highest, hitCount

def main():
    sample  = (20, 30), (-10, -5)
    myInput = (32, 65), (-225, -177)

    print(solve(sample))
    print(solve(myInput))

if __name__ == '__main__':
    main()
