import re
from collections import deque
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
   

   
def dfs_hash_flow(pressured_valves, a_path, b_path, elephant_mode):
    def secret_function(pressured_valves, a_path, b_path, dynamic_mem, elephant_mode, break_mem):
        global test_var
        max_release = 0
        # Get current hashstate
        pos = hash(a_path[-1][0].name + str(a_path[-1][1]))
        if elephant_mode:
            pos += hash(b_path[-1][0].name + str(b_path[-1][1]))
        valve_hash = 0
        for x in pressured_valves:
            valve_hash ^= hash(x.name)
        full_state = hash_state(pos, valve_hash)
        
        # Check if path is worth exploring
        pos_hash = hash(a_path[-1][0].name) + valve_hash
        time_data = [a_path[-1][1], a_path[-1][2]]
        if elephant_mode:
            pos_hash += hash(b_path[-1][0].name)
            time_data[0] += b_path[-1][1]
            time_data[1] += b_path[-1][2]
        if pos_hash in break_mem.keys():
            for x in break_mem[pos_hash].keys():
                if break_mem[pos_hash][x] >= time_data[1] and x >= time_data[0]:
                    # abort path
                    return 0
        
        # Check if path is already calculated
        if full_state in dynamic_mem.keys():
            max_release = dynamic_mem[full_state]
        else:        
            for i in range(len(pressured_valves)):
                # Temporarily remove valve so we don't visit an already visited valve
                tmp = pressured_valves.popleft()
                
                # Calculate new time after moving and turning valve
                a_time = a_path[-1][1] - a_path[-1][0].tunnels[tmp.name] - 1
                if a_time > 0:
                    # Add move to path
                    a_path.append((tmp, a_time, tmp.flow_dict[a_time] + a_path[-1][2]))
                    
                    result = secret_function(pressured_valves, a_path, b_path, dynamic_mem, elephant_mode, break_mem) 
                    
                    if result > max_release:
                        max_release = result
                    a_path.pop()
                
                if elephant_mode and a_path[-1][0].name != b_path[-1][0].name and a_path[-1][1] != b_path[-1][1]:
                    b_time = b_path[-1][1] - b_path[-1][0].tunnels[tmp.name] - 1
                    if b_time > 0:
                        # Add move to path
                        b_path.append((tmp, b_time, tmp.flow_dict[b_time] + b_path[-1][2]))
                        result = secret_function(pressured_valves, b_path, a_path, dynamic_mem, elephant_mode, break_mem) 
                        if result > max_release:
                            max_release = result
                        b_path.pop()
                        
                pressured_valves.append(tmp)
            # add result to memory    
            dynamic_mem[full_state] = max_release
            
            if pos_hash not in break_mem.keys():
                break_mem[pos_hash] = {}
            if not (time_data[0] in break_mem[pos_hash].keys() and time_data[1] < break_mem[pos_hash][time_data[0]]):
                break_mem[pos_hash][time_data[0]] = time_data[1]
            
        if a_path[-1][1] > 0:
            max_release += a_path[-1][0].flow_dict[a_path[-1][1]]
        
        
        if max_release > test_var:
            test_var = max_release
            #print(a_path[-1][2])
            print(test_var)
        
        return max_release  
    return secret_function(pressured_valves, a_path, b_path, {}, elephant_mode, {}) 

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
me_path.append((valves[start], total_time, 0))
dynamic_mem = {}
pressure_released = 0
pressure_released = dfs_hash_flow(pressured_valves, me_path, deque(), False)



print("The first answer is: ", pressure_released)

test_var = 0

# Part 2
total_time = 26
me_path = deque()
elephant_path = deque()
me_path.append((valves[start], total_time, 0))
elephant_path.append((valves[start], total_time, 0))
dynamic_mem = {}
pressure_released = dfs_hash_flow(pressured_valves, me_path, elephant_path, True)
print("The second answer is: ", pressure_released)

print("The execution time was: ", int((time.perf_counter()-timer)*1000), "ms")