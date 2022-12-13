import json
from functools import cmp_to_key

def compare(left, right):
    # Both ints check
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    # Both lists check
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)):
            if i >= len(right):
                return 1
            result = compare(left[i], right[i])
            if result != 0:
                return result
        if len(left) < len(right):
            return -1
    # One list and one int
    else:
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        return compare(left, right)
    return 0

# Read input
with open("day13input.txt") as f:
    data = [x.strip() for x in f.readlines()]
# Unpack strings with json
packets = []
for x in data:
    if x != '':
        packets.append(json.loads(x))
# Delete data since we don't need it anymore
del data

# Part one
ans = 0
for i in range(0, len(packets), 2):
    if compare(packets[i], packets[i+1]) == -1:
        # Add pair index to sum
        ans += i // 2 + 1
print("The first answer is: ", ans)

# Part two
# Add divider packets [[2]] [[6]]
divider_packets = [[[2]], [[6]]]
packets.append(divider_packets[0])
packets.append(divider_packets[1])
# Sort with custom compare
packets.sort(key=cmp_to_key(compare))
for i in range(len(packets)):
    # If a divider packet is found, save the index
    if packets[i] == divider_packets[0]:
        divider_packets[0] = i + 1
    if packets[i] == divider_packets[1]:
        divider_packets[1] = i + 1
print("The second answer is: ", divider_packets[0] * divider_packets[1])