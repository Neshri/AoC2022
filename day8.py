import numpy as np

# Read
with open("day8input.txt") as f:
    matrix = [[int(x) for x in y.strip()] for y in f.readlines()]
matrix = np.array(matrix)
visibility_matrix = np.zeros((len(matrix), len(matrix[0])), dtype=np.int32)
scenic_matrix = np.ones((len(matrix), len(matrix[0])), dtype=np.int64)
# Left to right
for y in range(len(matrix)):
    previous_heights = [0]*10
    height = -1
    for x in range(len(matrix[0])):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
        scenic_matrix[y][x] *= previous_heights[matrix[y][x]]
        i = 0
        while i <= matrix[y][x]:
            previous_heights[i] = 1
            i += 1
        while i < 10:
            previous_heights[i] += 1
            i += 1
# Right to left
for y in range(len(matrix)):
    previous_heights = [0]*10
    height = -1
    for x in reversed(range(len(matrix[0]))):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
        scenic_matrix[y][x] *= previous_heights[matrix[y][x]]
        i = 0
        while i <= matrix[y][x]:
            previous_heights[i] = 1
            i += 1
        while i < 10:
            previous_heights[i] += 1
            i += 1
# Down to up
for x in range(len(matrix[0])):
    previous_heights = [0]*10
    height = -1
    for y in range(len(matrix)):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
        scenic_matrix[y][x] *= previous_heights[matrix[y][x]]
        i = 0
        while i <= matrix[y][x]:
            previous_heights[i] = 1
            i += 1
        while i < 10:
            previous_heights[i] += 1
            i += 1
# Up to down
for x in range(len(matrix[0])):
    previous_heights = [0]*10
    height = -1
    for y in reversed(range(len(matrix))):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
        scenic_matrix[y][x] *= previous_heights[matrix[y][x]]
        i = 0
        while i <= matrix[y][x]:
            previous_heights[i] = 1
            i += 1
        while i < 10:
            previous_heights[i] += 1
            i += 1

# Part one
ans = 0
for y in range(len(matrix)):
    for x in range(len(matrix[0])):
        ans += visibility_matrix[y][x]
print("The first answer is: ", ans)
# Part two
ans = 0
for y in range(len(matrix)):
    for x in range(len(matrix[0])):
        if scenic_matrix[y][x] > ans:
            ans = scenic_matrix[y][x]
print("The second answer is: ", ans)
