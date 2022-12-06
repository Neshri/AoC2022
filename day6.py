from collections import deque
import time
t = time.perf_counter()

#Read
with open("day6input.txt") as f:
    data = f.readline().strip()

def detect_start(data, marker_length):
    ans = 0
    q = deque()
    for x in data[:marker_length-1]:
        q.append(x)
    i = marker_length-1
    while i < len(data):
        q.append(data[i])
        if len(q) > marker_length:
            q.popleft()
        ans = i + 1
        check = set()
        ans_found = True
        for x in q:
            if x in check:
                ans_found = False
                break
            else:
                check.add(x)
        if ans_found:
            break
        i += 1
    return ans

#Part one
print("The first answer is: ", detect_start(data, 4))
#Part two
print("The second answer is: ", detect_start(data, 14))
print("The execution time was: ", int((time.perf_counter()-t) * 1000), "ms")