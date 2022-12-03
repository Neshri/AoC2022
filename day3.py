#Util
def priority(ch):
    if ch.isupper():
        return ord(ch) - ord('A') + 27
    else:
        return ord(ch) - ord('a') + 1

#Reading
bags = []
with open("day3input.txt") as f:
    for l in f.readlines():
        l = l.strip()
        bags.append(l)

#Part one
ans = 0
for b in bags:
    left_set = set()
    for x in b[:len(b)//2]:
        left_set.add(x)
    item = 0
    for x in b[len(b)//2:]:
        if x in left_set:
            item = x
    ans += priority(item)
print("The first answer is: ", ans)

#Part two
ans = 0
for i in range(0, len(bags), 3):
    e_1 = set()
    for x in bags[i]:
        e_1.add(x)
    e_2 = set()
    for x in bags[i+1]:
        if x in e_1:
            e_2.add(x)
    e_3 = ''
    for x in bags[i+2]:
        if x in e_2:
            e_3 = x
    ans += priority(e_3)
print("The second answer is: ", ans)
