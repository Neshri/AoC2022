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
        self.flow_dict = {}
        for t in range(31):
            self.flow_dict[t] = flow_rate * t

    def __str__(self) -> str:
        return self.name + " : flow rate=" + str(self.flow_rate) + " : " + str(self.tunnels)

    def __repr__(self) -> str:
        return str(self)       
   
def dfs_hash_flow(pressured_valves, a_path, b_path, dynamic_mem, elephant_mode):
    max_release = 0
    
    # Get current hashstate
    pos = hash(a_path[-1][0].name + str(a_path[-1][1]))
    if elephant_mode:
        pos += hash(b_path[-1][0].name + str(b_path[-1][1]))
    valve_hash = 0
    for x in pressured_valves:
        valve_hash ^= hash(x.name)
    h = hash_state(pos, valve_hash)
    
    # h *= 1000
    # tmp = a_path[-1][1]
    # if elephant_mode:
    #     tmp *= b_path[-1][1]
    # h += tmp
    # TODO check if hashstate with less time left exist then return
    
    if h in dynamic_mem.keys():
        max_release = dynamic_mem[h]
    else:        
        for i in range(len(pressured_valves)):
            # Temporarily remove valve so we don't visit an already visited valve
            tmp = pressured_valves.popleft()
            
            # Calculate new time after moving and turning valve
            a_time = a_path[-1][1] - a_path[-1][0].tunnels[tmp.name] - 1
            if a_time > 0:
                # Add move to path
                a_path.append((tmp, a_time))
                result = dfs_hash_flow(pressured_valves, a_path, b_path, dynamic_mem, elephant_mode) 
                if result > max_release:
                    max_release = result
                a_path.pop()
            
            if elephant_mode and a_path[-1][0].name != b_path[-1][0].name:
                b_time = b_path[-1][1] - b_path[-1][0].tunnels[tmp.name] - 1
                if b_time > 0:
                    # Add move to path
                    b_path.append((tmp, b_time))
                    result = dfs_hash_flow(pressured_valves, b_path, a_path, dynamic_mem, elephant_mode) 
                    if result > max_release:
                        max_release = result
                    b_path.pop()
                    
            pressured_valves.append(tmp)
            
        dynamic_mem[h] = max_release
        
    if a_path[-1][1] > 0:
        max_release += a_path[-1][0].flow_dict[a_path[-1][1]]
    
    global test_var
    if max_release > test_var:
        test_var = max_release
        print(test_var)
    
    return max_release   

def hash_state(pos, unopened_valves):
    return pos * unopened_valves
 
     
# Read and create pipe network
valves = {}
with open("day16input.txt") as f:
#with open("test.txt") as f:
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
# Collect valves containing pressure
pressured_valves = []
for v in valves.values():
    if v.flow_rate > 0:
        pressured_valves.append(v)

test_var = 0

pressured_valves = deque(pressured_valves)
me_path = deque()
me_path.append((valves[start], total_time))
dynamic_mem = {}
pressure_released = 0
pressure_released = dfs_hash_flow(pressured_valves, me_path, deque(), dynamic_mem, False)



print("The first answer is: ", pressure_released)

test_var = 0

# Part 2
total_time = 26
me_path = deque()
elephant_path = deque()
me_path.append((valves[start], total_time))
elephant_path.append((valves[start], total_time))
dynamic_mem = {}
pressure_released = dfs_hash_flow(pressured_valves, me_path, elephant_path, dynamic_mem, True)
print("The second answer is: ", pressure_released)

print("The execution time was: ", int((time.perf_counter()-timer)*1000), "ms")