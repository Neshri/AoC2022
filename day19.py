import re
import time
t = time.perf_counter()

BITMASKS = {"geode": 0xFFFF << 48, "obsidian": 0xFFFF << 32, "clay": 0xFFFF << 16, "ore": 0xFFFF}

class Blueprint:
    def __init__(self, bp) -> None:
        def get_cost(string):
            cost = re.findall("\d+ \w+", string)
            send_d = {}
            for x in cost:
                spl = x.split(" ")
                i = int(spl[0])
                send_d[spl[1]] = i
            return send_d
        
        string = re.findall("Each ore robot [ A-Za-z0-9]+", bp)[0]
        self.ore_robot = get_cost(string)
        string = re.findall("Each clay robot [ A-Za-z0-9]+", bp)[0]
        self.clay_robot = get_cost(string)
        string = re.findall("Each obsidian robot [ A-Za-z0-9]+", bp)[0]
        self.obsidian_robot = get_cost(string)
        string = re.findall("Each geode robot [ A-Za-z0-9]+", bp)[0]
        self.geode_robot = get_cost(string)

def dict_hash(d):
    hash_value = 0
    for key in d.keys():
        hash_value += hash((hash(d[key]), hash(key)))
    return hash_value

        
def max_g_crack(time_limit, bp):
    
    hash_check = dict()
    costs = {"geode": bp.geode_robot, "obsidian": bp.obsidian_robot, "clay": bp.clay_robot, "ore": bp.ore_robot}
    def recursive_crack(time_limit, resources, robots, best_crack):
        # Bottom reached
        if time_limit <= 0:
            return best_crack
        
        # Optimiziation pruning
        max_bot_need = {"geode": float("inf"), "obsidian": 0, "clay": 0, "ore": 0}
        for k in costs.keys():
            for k2 in costs[k].keys():
                if costs[k][k2] > max_bot_need[k2]:
                    max_bot_need[k2] = costs[k][k2]
        
        if costs["geode"]["obsidian"] < robots["obsidian"] or costs["obsidian"]["clay"] < robots["clay"]:
            return best_crack
        
        
        for i in range(1, time_limit + 1):
            time_left = time_limit - i
            if resources["geode"] + robots["geode"] * (time_left + 1) + (time_left * time_left + time_left) / 2 <= best_crack:
                return best_crack    
            
            building = list()     
            # Start bot building
            for k in ["geode", "obsidian", "clay", "ore"]:
                cost = costs[k]
                can_afford = True
                for x in cost.keys():
                    if cost[x] > resources[x]:
                        can_afford = False
                        break
                if can_afford and robots[k] < max_bot_need[k]:
                    building.append(k)
                    
            # Drilling
            for x in robots.keys():
                resources[x] += robots[x]
            
            # Finish bot building   
            for robot in building:
                new_resources = dict(resources)
                new_robots = dict(robots)
                cost = costs[robot]
                for x in cost.keys():
                    new_resources[x] -= cost[x]
                new_robots[robot] += 1
                hash_value = (dict_hash(new_resources), dict_hash(new_robots))
                
                
                
                if (hash_value not in hash_check.keys() or 
                    hash_check[hash_value][1] < time_limit - i):
                    
                    tmp = recursive_crack(time_limit - i, dict(new_resources), new_robots, best_crack)
                    if hash_value not in hash_check.keys() or hash_check[hash_value][0] < tmp:
                        hash_check[hash_value] = (tmp, time_limit - i)
                        # print(hash_check[hash_value])
                else:
                    tmp = hash_check[hash_value][0]
                if tmp > best_crack:
                    best_crack = tmp
                
        
        if resources["geode"] > best_crack:
            best_crack = resources["geode"]
        return best_crack
    
    resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    # resources = 0
    # robots = 1
    
    ans = recursive_crack(time_limit, resources, robots, 0)
    return ans


with open("day19input.txt") as f:
    blueprints = [x.strip() for x in f.readlines()]

for i in range(len(blueprints)):
    bp = Blueprint(blueprints[i])
    blueprints[i] = bp
# Part 1
ans = 0
for i in range(len(blueprints)):
    cracked = max_g_crack(24, blueprints[i])
    print(cracked, i)
    ans += cracked * (i + 1)
    # print(ans)
print("The first answer is:", ans)

# Part 2
ans = 1
for bp in blueprints[:3]:
    cracked = max_g_crack(32, bp)
    ans *= cracked
    print(ans)
print("The second answer is:", ans)
    
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")