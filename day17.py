CHAMBER_WALLS = (0, 7)
class Shape:
    
    def __init__(self, rock_type, pos) -> None:
        self.points = set()
        self.lo_x, self.hi_x, self.lo_y, self.hi_y = 0, 0, 0, 0
        # Create rock of given type and realign position so that its left edge is 
        # two units away from the left wall and its bottom edge is three units 
        # above the highest rock in the room (or the floor, if there isn't one).
        
        # xxxx
        if rock_type == 0:
            self.lo_x = 0
            self.hi_x = 3
            self.lo_y = 0
            self.hi_y = 0
            for i in range(4):
                self.points.add((i, 0))
        # .x.
        # xxx
        # .x.
        elif rock_type == 1:
            self.lo_x = 0
            self.hi_x = 2
            self.lo_y = 0
            self.hi_y = 2
            self.points.add((1, 0))
            for i in range(3):
                self.points.add((i, 1))
            self.points.add((1, 2))
        # ..x
        # ..x
        # xxx
        elif rock_type == 2:
            self.lo_x = 0
            self.hi_x = 2
            self.lo_y = 0
            self.hi_y = 2
            for i in range(3):
                self.points.add((i, 0))
                self.points.add((2, i))
        # x
        # x
        # x
        # x
        elif rock_type == 3:
            self.lo_x = 0
            self.hi_x = 0
            self.lo_y = 0
            self.hi_y = 3
            for i in range(4):
                self.points.add((0, i))
        # xx
        # xx
        elif rock_type == 4:
            self.lo_x = 0
            self.hi_x = 1
            self.lo_y = 0
            self.hi_y = 1
            for i in range(2):
                self.points.add((i, 0))
                self.points.add((i, 1))
        self.pos = [pos[0], pos[1]]

    def move(self, x, y, chamber):
        moved = True
        if (CHAMBER_WALLS[0] <= self.pos[0] + self.lo_x + x and 
            self.pos[0] + self.hi_x + x < CHAMBER_WALLS[1] and 
            self.pos[1] + y + self.lo_y >= 0):
            for p in self.points:
                if (p[0] + self.pos[0] + x, p[1] + self.pos[1] + y) in chamber:
                    moved = False
                    break
            if moved:
                self.pos[0] += x
                self.pos[1] += y

        else:
            moved = False
        return moved

with open("day17input.txt") as f:
    instr = f.readline().strip()

   
def run_simulation(Shape, instr, number_of_rocks):
    chamber = set()
    i_index = 0
    rock_index = 0
    rock_counter = 0
    pos = [2, 3]
    highest_point = 0
    last_high = 0
    
    while rock_counter < number_of_rocks:
        # 3 4 2 1 3 3 2 0 1 2 2 1 0 0 3 2 2 0 1 2 3 0 0 1
        # if rock_counter % 10000 == 0:
        
        print(highest_point - last_high)
        current_rock = Shape(rock_index, pos)
        step_count = 0
        while True:
            step_count += 1
            if instr[i_index] == '<':
                x = -1
            else:
                x = 1
            i_index += 1
            i_index %= len(instr)
        # JetPush the rock
            current_rock.move(x, 0, chamber)
        # GravityMove the rock
            has_moved = current_rock.move(0, -1, chamber)
            if not has_moved:
                for p in current_rock.points:
                    chamber.add((p[0] + current_rock.pos[0], p[1] + current_rock.pos[1]))
                break
        if current_rock.pos[1] + current_rock.hi_y > highest_point:
            last_high = highest_point
            highest_point = current_rock.pos[1] + current_rock.hi_y
        pos = [2, highest_point + 4]
        rock_index += 1
        rock_index = rock_index % 5
        rock_counter += 1
    return highest_point

highest_point = run_simulation(Shape, instr, 2022)
print("The first answer is: ", highest_point+1)

# highest_point = run_simulation(Shape, instr, 1000000000000)
print(highest_point+1)

