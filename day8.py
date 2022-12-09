import numpy as np

#Read
with open("day8input.txt") as f:
    matrix = [[int(x) for x in y.strip()] for y in f.readlines()]
matrix = np.array(matrix)
visibility_matrix = np.zeros((len(matrix), len(matrix[0])), dtype=np.int32)
scenic_matrix = np.ones((len(matrix), len(matrix[0])), dtype=np.int64)
#Left to right
for y in range(len(matrix)):
    scene_score = 0
    height = -1
    for x in range(len(matrix[0])):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
        scenic_matrix[y][x] *= scene_score
            
#Right to left
for y in range(len(matrix)):
    height = -1
    for x in reversed(range(len(matrix[0]))):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
#Down to up
for x in range(len(matrix[0])):
    height = -1
    for y in range(len(matrix)):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1
#Up to down
for x in range(len(matrix[0])):
    height = -1
    for y in reversed(range(len(matrix))):
        if matrix[y][x] > height:
            height = matrix[y][x]
            visibility_matrix[y][x] = 1

#Part one
ans = 0
for y in range(len(matrix)):
    for x in range(len(matrix[0])):
        ans += visibility_matrix[y][x]
print("The first answer is: ", ans)
#Part two
ans = 0
for y in range(len(matrix)):
    for x in range(len(matrix[0])):
        if scenic_matrix[y][x] > ans:
            ans = scenic_matrix[y][x]
print("The second answer is: ", ans)