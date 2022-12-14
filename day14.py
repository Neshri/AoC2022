import time
t = time.perf_counter()

# Return True if void reached
def drop_sand_into_void(x, y, y_max, cave):
    while True:
        if y > y_max:
            return True
        if cave[y + 1][x] == ' ':
            y += 1
        elif cave[y+1][x-1] == ' ':
            y += 1
            x -= 1
        elif cave[y+1][x+1] == ' ':
            y += 1
            x += 1
        else:
            break
    cave[y][x] = 'o'
    return False

# Return True if source is plugged
def drop_sand_on_endless_floor(x, y, y_max, cave):
    start = (x, y)
    while True:
        #print(x, y)
        if y == y_max + 1:
            break
        if cave[y + 1][x] == ' ':
            y += 1
        elif cave[y+1][x-1] == ' ':
            y += 1
            x -= 1
        elif cave[y+1][x+1] == ' ':
            y += 1
            x += 1
        else:
            break
    cave[y][x] = 'o'
    return (x, y) == start

# Read and find min and max values
with open("day14input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
cave_lines = []
x_min, x_max = 2**63, -2**63
y_min, y_max = 2**63, -2**63
for line in lines:
    tmp = line.split(" -> ")
    shape = []
    for p in tmp:
        p = [int(x) for x in p.split(',')]
        shape.append(p[0])
        shape.append(p[1])
        if p[0] < x_min:
            x_min = p[0]
        elif p[0] > x_max:
            x_max = p[0]
        if p[1] < y_min:
            y_min = p[1]
        elif p[1] > y_max:
            y_max = p[1]
    cave_lines.append(shape)
print("X range is: ", x_min, "-", x_max)
print("Y range is: ", y_min, "-", y_max)

# Create cave to simulate
cave = []
for i in range(y_max+3):
    cave.append([' ']*(x_max+y_max))
for lines in cave_lines:
    previous = [lines[0], lines[1]]
    for i in range(2, len(lines), 2):
        # Draw horizontal lines
        x_dir = 1 if previous[0] < lines[i] else -1
        for x in range(previous[0], lines[i] + x_dir, x_dir):
            cave[previous[1]][x] = '#'
        # Draw vertical lines
        y_dir = 1 if previous[1] < lines[i+1] else -1
        for y in range(previous[1], lines[i+1] + y_dir, y_dir):
            cave[y][previous[0]] = '#'
        previous[0] = lines[i]
        previous[1] = lines[i+1]

# Part one
sand_counter = 0
while not drop_sand_into_void(500, 0, y_max, cave):
    sand_counter += 1
print("Grains of sand before void was reached: ", sand_counter)

# Clean the cave
for y in range(len(cave)):
    for x in range(len(cave[y])):
        if cave[y][x] == 'o':
            cave[y][x] = ' '
# Part two
# Start counter at 1 since while loop breaks before adding the last grain
sand_counter = 1
while not drop_sand_on_endless_floor(500, 0, y_max, cave):
    sand_counter += 1
print("Grains of sand before source was plugged: ", sand_counter)
print("The execution time was: ", int((time.perf_counter()-t)*1000), "ms")