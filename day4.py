
def contains(a, b):
    if a[0] <= b[0] and b[1] <= a[1]:
        return True
    if b[0] <= a[0] and a[1] <= b[1]:
        return True
    return False

def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

with open("day4input.txt") as f:
    sections = [x.strip().split(',') for x in f.readlines()]
ans = 0
ans_2 = 0
for x in sections:
    x[0] = [int(y) for y in x[0].split('-')]
    x[1] = [int(y) for y in x[1].split('-')]
    if contains(x[0], x[1]):
        ans += 1
        ans_2 += 1
    elif overlaps(x[0], x[1]):
        ans_2 += 1
print("The first answer is: ", ans)
print("The second answer is: ", ans_2)