from collections import deque

def try_walk(a, b, matrix, steps, queue, visits, going_up):
    if 0 <= a[0] < len(matrix) and 0 <= b[0] < len(matrix):
        if  0 <= a[1] < len(matrix[a[0]]) and 0 <= b[1] < len(matrix[b[0]]):
            a_height = matrix[a[0]][a[1]]
            if a_height == 'S':
                a_height = 'a'
            elif a_height == 'E':
                a_height = 'z'
            b_height = matrix[b[0]][b[1]]
            if b_height == 'S':
                b_height = 'a'
            elif b_height == 'E':
                b_height = 'z'
            if going_up:
                diff = ord(b_height) - ord(a_height)
            else:
                diff = ord(a_height) - ord(b_height)
            if diff <= 1:
                if b in visits.keys():
                    if steps+1 < visits[b]:
                        visits[b] = steps+1
                        queue.append((b, steps+1))
                else:
                    visits[b] = steps+1
                    queue.append((b, steps+1))
# Read
with open("day12input.txt") as f:
    matrix = [x.strip() for x in f.readlines()]
# Find start and end
start = 0
end = 0
for y in range(len(matrix)):
    for x in range(len(matrix[y])):
        if matrix[y][x] == 'S':
            start = (y, x)
        elif matrix[y][x] == 'E':
            end = (y, x)

# Part 1
visits = {}
queue = deque()
visits[start] = 0
queue.append((start, 0))
while queue:
    pos, steps = queue.popleft()
    height = matrix[pos[0]][pos[1]]
    # Look down
    new_pos = (pos[0]-1, pos[1])
    try_walk(pos, new_pos, matrix, steps, queue, visits, True)
    # Look up
    new_pos = (pos[0]+1, pos[1])
    try_walk(pos, new_pos, matrix, steps, queue, visits, True)
    # Look left
    new_pos = (pos[0], pos[1]-1)
    try_walk(pos, new_pos, matrix, steps, queue, visits, True)
    # Look right
    new_pos = (pos[0], pos[1]+1)
    try_walk(pos, new_pos, matrix, steps, queue, visits, True)
print("The first answer is: ", visits[end])

# Part 2
visits = {}
queue = deque()
visits[end] = 0
queue.append((end, 0))
while queue:
    pos, steps = queue.popleft()
    height = matrix[pos[0]][pos[1]]
    # Look down
    new_pos = (pos[0]-1, pos[1])
    try_walk(pos, new_pos, matrix, steps, queue, visits, False)
    # Look up
    new_pos = (pos[0]+1, pos[1])
    try_walk(pos, new_pos, matrix, steps, queue, visits, False)
    # Look left
    new_pos = (pos[0], pos[1]-1)
    try_walk(pos, new_pos, matrix, steps, queue, visits, False)
    # Look right
    new_pos = (pos[0], pos[1]+1)
    try_walk(pos, new_pos, matrix, steps, queue, visits, False)
ans = 2**128
for y in range(len(matrix)):
    for x in range(len(matrix[y])):
        if matrix[y][x] == 'a':
            if (y, x) in visits.keys():
                if visits[(y, x)] < ans:
                    ans = visits[(y, x)]
print("The second answer is: ", ans)