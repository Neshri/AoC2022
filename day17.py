
class Shape:
    
    def __init__(self, rock_type, pos) -> None:
        self.points = set()
        # Create rock of given type and realign position so that its left edge is 
        # two units away from the left wall and its bottom edge is three units 
        # above the highest rock in the room (or the floor, if there isn't one).
        if rock_type == 0:
            for i in range(4):
                self.points.add((i, 0))
        elif rock_type == 1:
            pos[1] -= 2
            self.points.add((1, 0))
            for i in range(3):
                self.points.add((i, 1))
            self.points.add((1, 2))
        elif rock_type == 2:
            pos[1] -= 2
            for i in range(3):
                self.points.add((i, 2))
                self.points.add((2, i))
        elif rock_type == 3:
            pos[1] -= 3
            for i in range(4):
                self.points.add((0, i))
        elif rock_type == 4:
            pos[1] -= 1
            for i in range(2):
                self.points.add((i, 0))
                self.points.add((i, 1))
        self.pos = [pos[0], pos[1]]

with open("day17input.txt") as f:
    instr = f.readline().strip()
    
chamber = set()
i_index = 0
rock_index = 0
rock_counter = 0
pos = [2, 3]
while rock_counter < 2022:
    current_rock = Shape(rock_index, pos)
    
    rock_index += 1
    rock_index = rock_index % 5
    rock_counter += 1
