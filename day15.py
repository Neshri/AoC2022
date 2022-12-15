import re
import time

t = time.perf_counter()

class Sensor:

    def __init__(self, x, y, closest_beacon) -> None:
        self.x = x
        self.y = y
        self.closest_beacon = closest_beacon
        self.distance_to_beacon = abs(x - closest_beacon[0]) + abs(y - closest_beacon[1])

    def no_beacon_range(self, y):
        if abs(self.y - y) > self.distance_to_beacon:
            return -1
        dist = self.distance_to_beacon - abs(self.y - y)
        result = [self.x - dist, self.x + dist]
        if self.closest_beacon[1] == y:
            if dist == 0:
                return -1
            if self.closest_beacon[0] == result[0]:
                result[0] += 1
            elif self.closest_beacon[0] == result[1]:
                result[1] -= 1
        return result

def get_no_beacon_ranges(sensors, row_to_check):
    nbranges = []
    for s in sensors:
        result = s.no_beacon_range(row_to_check)
        if result != -1:
            nbranges.append(result)
    # Sort and combine ranges so there's no overlap
    nbranges.sort()
    combined_ranges = set()
    tmp_range = [nbranges[0][0], nbranges[0][1]]
    for r in nbranges[1:]:
        if tmp_range[1] >= r[0]:
            if r[1] > tmp_range[1]:
                tmp_range[1] = r[1]
        else:
            combined_ranges.add((tmp_range[0], tmp_range[1]))
            tmp_range = [r[0], r[1]]
    combined_ranges.add((tmp_range[0], tmp_range[1]))
    del nbranges
    del tmp_range
    return combined_ranges

def areas_touching(a, b):
    wanted_dist = a.distance_to_beacon + b.distance_to_beacon + 1
    actual_dist = manhattan_distance((a.x, a.y), (b.x, b.y))
    return wanted_dist >= actual_dist

def find_adjacent_point(sensors):
    x = [0, 0]
    y = [0, 0]
    x[0] = sensors[0].x - sensors[0].distance_to_beacon - 1
    x[1] = sensors[0].x + sensors[0].distance_to_beacon + 1
    y[0] = sensors[0].y - sensors[0].distance_to_beacon - 1
    y[1] = sensors[0].y + sensors[0].distance_to_beacon + 1
    for s in sensors:
        n = s.x - s.distance_to_beacon - 1
        if n > x[0]:
            x[0] = min(n, x[1])
        n = s.x + s.distance_to_beacon + 1
        if n < x[1]:
            x[1] = max(n, x[0])
        n = s.y - s.distance_to_beacon - 1
        if n > y[0]:
            y[0] = min(n, y[1])
        n = s.y + s.distance_to_beacon + 1
        if n < y[1]:
            y[1] = max(n, y[0])
    # 3299359 3355220
    if x[0] <= 3299359 <= x[1] and y[0] <= 3355220 <= y[1]:
        print(x, y)
    x = 0
    y = 0
    for s in sensors:
        if manhattan_distance((x, y), (s.x, s.y)) != s.distance_to_beacon + 1:
            return -1
    return (x, y)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Read and extract numbers from input
with open("day15input.txt") as f:
    lines = [re.findall("-*\d+", x) for x in f.readlines()]
for i in range(len(lines)):
    lines[i] = [int(x) for x in lines[i]]
sensors = []
beacons = set()
min_y, max_y = 2**63, -2**63
for l in lines:
    beacons.add((l[2], l[3]))
    if l[1] < min_y:
        min_y = l[1]
    elif l[1] > max_y:
        max_y = l[1]
    sensors.append(Sensor(l[0], l[1], (l[2], l[3])))

# Part one: In the row where y=2000000, how many positions cannot contain a beacon?
row_to_check = 2000000
ranges = get_no_beacon_ranges(sensors, row_to_check)
# Sum the ranges to get the answer
ans = 0
for x in ranges:
    # +1 so the range is inclusive
    ans += x[1] - x[0] + 1
print("The first answer is: ", ans)

# Part 2: Tuning frequency = X * 4000000 + Y
# 0 <= X,Y <= 4000000
# Find the hidden distress beacon. What is its tuning frequency?
ans_found = False
max_coord = 4000000
beacon_x, beacon_y = 0, 0

min_y = min_y if min_y >= 0 else 0
max_y = max_y if max_y <= max_coord else max_coord
print(min_y, max_y)
for y in range(min_y, max_y):
    if ans_found:
        break
    ranges = list(get_no_beacon_ranges(sensors, y))
    if len(ranges) > 0:
        ranges.sort()
        ranges.append([ranges[-1][1]+2])
        for r in ranges:
            x = r[0] - 1    
            if 0 <= x <= max_coord:
                if (x, y) not in beacons:
                    beacon_x = x
                    beacon_y = y
                    ans_found = True
                    break


# Circumference b_dist + 1 = x + y + 1
# beacon_x = [0, max_coord]
# beacon_y = [0, max_coord]
# for i in range(len(sensors)):
#     touch_count = 0
#     touch_list = []
#     for j in range(len(sensors)):
#         if i != j and areas_touching(sensors[i], sensors[j]):
#             touches_all = True
#             for t in touch_list:
#                 if not areas_touching(sensors[t], sensors[j]):
#                     touches_all = False
#                     break
#             if touches_all:
#                 touch_count += 1
#                 touch_list.append(j)
#     if touch_count >= 3:
#         for t in range(len(touch_list)):
#             touch_list[t] = sensors[touch_list[t]]
#         tmp = find_adjacent_point(touch_list)
#         if tmp != -1 and tmp not in beacons:
#             beacon_x = tmp[0]
#             beacon_y = tmp[1]
#             break
        
# 3299359 3355220
print(beacon_x, beacon_y)
print("The second answer is: ", beacon_x * max_coord + beacon_y)
print("The execution time was: ", int((time.perf_counter() - t) * 1000), "ms")