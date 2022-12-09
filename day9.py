# Y, X
def move(rope, visited, direction):
    if direction == 'U':
        rope[0][0] += 1
    elif direction == 'D':
        rope[0][0] -= 1
    elif direction == 'L':
        rope[0][1] -= 1
    elif direction == 'R':
        rope[0][1] += 1
    for i in range(1, len(rope)):
        if abs(rope[i-1][0] - rope[i][0]) > 1 or abs(rope[i-1][1] - rope[i][1]) > 1:
            if rope[i-1][0] != rope[i][0]:
                y = (rope[i-1][0] - rope[i][0]) // abs(rope[i-1][0] - rope[i][0])
            else:
                y = 0
            if rope[i-1][1] != rope[i][1]:
                x = (rope[i-1][1] - rope[i][1]) // abs(rope[i-1][1] - rope[i][1])
            else:
                x = 0
        else:
            y, x = 0, 0
        rope[i][0] += y
        rope[i][1] += x
    visited.add((rope[len(rope)-1][0], rope[len(rope)-1][1]))
    
# Read
with open("day9input.txt") as f:
    instructions = [x.strip() for x in f.readlines()]
rope = [[0, 0], [0, 0]]
visited = set()
visited.add((0, 0))

# Part one
for instr in instructions:
    d, l = instr.split(' ')
    l = int(l)
    for i in range(l):
        move(rope, visited, d)
print("The first answer is: ", len(visited))

# Part two
visited = set()
rope = []
for i in range(10):
    rope.append([0, 0])
for instr in instructions:
    d, l = instr.split(' ')
    l = int(l)
    for i in range(l):
        move(rope, visited, d)
print("The second answer is: ", len(visited))