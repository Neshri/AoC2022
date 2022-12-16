import re
from collections import deque
from functools import cmp_to_key
import time
timer = time.perf_counter()


class Valve:

    def __init__(self, name, flow_rate, tunnels) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = {}
        for t in tunnels:
            self.tunnels[t] = 1
        self.opened = False

    def __str__(self) -> str:
        return self.name + " : flow rate=" + str(self.flow_rate) + " : " + str(self.tunnels)

    def __repr__(self) -> str:
        return str(self)


# Read and create pipe network
valves = {}
with open("day16input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        names = re.findall("[A-Z]{2}", line)
        flow_rate = int(re.findall("=\d+", line)[0][1:])
        v = Valve(names[0], flow_rate, names[1:])
        valves[v.name] = v
for v in valves.values():
    q = deque()
    visited = set()
    q.append((v, 0))
    visited.add(v.name)
    while q:
        current, cost = q.popleft()
        for x in current.tunnels.keys():
            if x not in visited or x in v.tunnels.keys() and v.tunnels[x] > cost + current.tunnels[x]:
                v.tunnels[x] = cost + current.tunnels[x]
                visited.add(x)
                q.append((valves[x], v.tunnels[x]))
            

# Part 1
total_time = 30
start = "AA"
pressure_released = 0
current = valves[start]
pressured_valves = []
for v in valves.values():
    if v.flow_rate > 0:
        pressured_valves.append(v)



def recurse(current, pressured_valves, time_left) -> int:
    if time_left <= 0:
        return 0
    pressured_valves = deque(pressured_valves)
    max_pressure_release = 0
    for i in range(len(pressured_valves)):
        tmp = pressured_valves.popleft()
        result = recurse(tmp, list(pressured_valves), time_left - (current.tunnels[tmp.name] + 1))
        pressured_valves.append(tmp)
        if result > max_pressure_release:
            max_pressure_release = result
    max_pressure_release += current.flow_rate * time_left
    return max_pressure_release

def recurse_with_elephant(my_pos, elephant_pos, pressured_valves, time_left) -> int:
    if time_left <= 0:
        return 0
    pressured_valves = deque(pressured_valves)
    max_pressure_release = 0
    for i in range(len(pressured_valves)):
        tmp = pressured_valves.popleft()
        for j in range(len(pressured_valves)):
            tmp_2 = pressured_valves.popleft()
            result = recurse_with_elephant(tmp, tmp_2, list(pressured_valves), time_left - (my_pos.tunnels[tmp.name] + 1))
            pressured_valves.append(tmp_2)
        pressured_valves.append(tmp)
        if result > max_pressure_release:
            max_pressure_release = result
    max_pressure_release += my_pos.flow_rate * time_left
    return max_pressure_release

pressure_released = recurse(valves[start], [x for x in pressured_valves], total_time)

# while total_time > 0:
#     print(current)
#     print(total_time)
#     print(pressure_released)
#     def compare(a, b): return a.flow_rate * (total_time - current.tunnels[a.name] - 1) - b.flow_rate * (total_time - current.tunnels[b.name] - 1)
#     pressured_valves.sort(key=cmp_to_key(compare), reverse=True)

#     if not pressured_valves:
#         break
#     next = pressured_valves.pop(0)
#     while pressured_valves and total_time < (current.tunnels[next.name] + 1):
#         next = pressured_valves.pop(0)

#     total_time = total_time - (current.tunnels[next.name] + 1)
#     if total_time <= 0:
#         break
#     pressure_released += next.flow_rate * total_time
#     current = next

print("The first answer is: ", pressure_released)




total_time = 26


print("The second answer is: ", pressure_released)

print("The execution time was: ", int((time.perf_counter()-timer)*1000), "ms")