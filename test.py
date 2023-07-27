import re
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

def max_g_crack(time_limit, bp):
    max_geodes = [[0] * (time_limit + 1) for _ in range(5)]

    for t in range(1, time_limit + 1):
        for robot in range(1, 5):
            max_geodes[robot][t] = max_geodes[robot][t - 1]
            cost = get_cost(bp, robot)
            if t >= cost:
                max_geodes[robot][t] = max(max_geodes[robot][t], max_geodes[robot][t - cost] + 1)

    return max_geodes[4][time_limit]

def get_cost(bp, robot):
    if robot == 1:
        return bp.ore_robot["ore"]
    elif robot == 2:
        return bp.clay_robot["ore"]
    elif robot == 3:
        return bp.obsidian_robot["ore"] + bp.obsidian_robot["clay"]
    elif robot == 4:
        return bp.geode_robot["ore"] + bp.geode_robot["obsidian"]

# Example usage:
bp = Blueprint("Each ore robot costs 4 ore\nEach clay robot costs 2 ore\nEach obsidian robot costs 3 ore and 14 clay\nEach geode robot costs 2 ore and 7 obsidian")
time_limit = 24
max_geodes = max_g_crack(time_limit, bp)
print(max_geodes)
