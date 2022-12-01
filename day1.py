elves = []

with open("day1input.txt") as f:
    elf = []
    for x in f.readlines():
        n = x.strip()
        if n == '':
            elves.append(elf)
            elf = []
        else:
            n = int(n)
            elf.append(n)
sums = []
ans = 0
for e in elves:
    s = sum(e)
    sums.append(s)
    if s > ans:
        ans = s

print("The first answer is: ", ans)
sums.sort(reverse=True)
print("The second answer is: ", sum(sums[:3]))