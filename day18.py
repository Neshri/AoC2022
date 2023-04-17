import time
from collections import deque
t = time.perf_counter()

def out_of_bounds(point, bounds):
    return not(bounds[0] <= point[0] <= bounds[1] and bounds[2] <= point[1] <= bounds[3] and bounds[4] <= point[2] <= bounds[5])


with open("day18input.txt") as f:
    cubes = [[int(y) for y in x.strip().split(",")] for x in f.readlines()]
cube_hash = set()
min_x, max_x, min_y, max_y, min_z, max_z = 0, 0, 0, 0, 0, 0
for c in cubes:
    if c[0] < min_x:
        min_x = c[0]
    elif c[0] > max_x:
        max_x = c[0]
    if c[1] < min_y:
        min_y = c[1]
    elif c[1] > max_y:
        max_y = c[1]
    if c[2] < min_z:
        min_z = c[2]
    elif c[2] > max_z:
        max_z = c[2]
    cube_hash.add(tuple(c))
surface_area = 0
for c in cubes:
    tmp_area = 0
    if (c[0] - 1, c[1], c[2]) not in cube_hash:
        tmp_area += 1
    if (c[0] + 1, c[1], c[2]) not in cube_hash:
        tmp_area += 1
    if (c[0], c[1] - 1, c[2]) not in cube_hash:
        tmp_area += 1
    if (c[0], c[1] + 1, c[2]) not in cube_hash:
        tmp_area += 1
    if (c[0], c[1], c[2] - 1) not in cube_hash:
        tmp_area += 1
    if (c[0], c[1], c[2] + 1) not in cube_hash:
        tmp_area += 1
    surface_area += tmp_area

print("The first answer is: ", surface_area)

min_x -= 1
min_y -= 1
min_z -= 1
max_x += 1
max_y += 1
max_z += 1
# DFS through bounding box/outside air/steam
bounds = (min_x, max_x, min_y, max_y, min_z, max_z)
surface_area = 0
empty_visits = set()
current_point = (min_x, min_y, min_z)
queue = deque()
queue.append(current_point)
empty_visits.add(current_point)
while queue:
    current_point = queue.pop()
    # Look around current point
    test_points = [(current_point[0] - 1, current_point[1], current_point[2])]
    test_points.append((current_point[0] + 1, current_point[1], current_point[2]))
    test_points.append((current_point[0], current_point[1] - 1, current_point[2]))
    test_points.append((current_point[0], current_point[1] + 1, current_point[2]))
    test_points.append((current_point[0], current_point[1], current_point[2] - 1))
    test_points.append((current_point[0], current_point[1], current_point[2] + 1))
    for i in range(len(test_points)):
        if test_points[i] in cube_hash:
            # Steam adjacent to lava
            surface_area += 1
        elif test_points[i] not in empty_visits and not out_of_bounds(test_points[i], bounds):
            empty_visits.add(test_points[i])
            queue.append(test_points[i])
   
print("The second answer is: ", surface_area)
 
print("The execution time was: ", int((time.perf_counter() - t) * 1000), "ms")