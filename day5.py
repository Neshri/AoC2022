from collections import deque

#Reading
instructions = []
original_crates = {}
nbr_of_stacks = 0
with open("day5input.txt") as f:
    for line in f.readlines():
        line = line.rstrip()
        if line.startswith("move"):
            line = line.split(' ')
            instructions.append((int(line[1]), int(line[3]), int(line[5])))
        else:
            for i in range(len(line)):
                if line[i].isalpha():
                    # 1=1 2=5 3=9 4=13
                    index = (i-1) // 4 + 1
                    if index > nbr_of_stacks:
                        nbr_of_stacks = index
                    if index not in original_crates.keys():
                        original_crates[index] = deque()
                    original_crates[index].append(line[i])
#Copy
crates = {}
for k in original_crates.keys():
    crates[k] = deque()
    for x in original_crates[k]:
        crates[k].append(x)

#Part one
for instr in instructions:
    for i in range(instr[0]):
        tmp = crates[instr[1]].popleft()
        crates[instr[2]].appendleft(tmp)
ans = ''
for i in range(1, nbr_of_stacks+1):
    if crates[i]:
        ans += crates[i][0]
print("The first answer is: ", ans)
            
#Part two
crates = original_crates
for instr in instructions:
    tmp = deque()
    for i in range(instr[0]):
        tmp.appendleft(crates[instr[1]].popleft())
    crates[instr[2]].extendleft(tmp)
ans = ''
for i in range(1, nbr_of_stacks+1):
    if crates[i]:
        ans += crates[i][0]
print("The second answer is: ", ans)