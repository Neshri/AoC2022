from collections import deque

class Directory:
    def __init__(self, parent, name) -> None:
        self.dirs = dict()
        self.files = dict()
        self.parent = parent
        self.name = name

    def print_tree(self, prefix):
        print("d" + prefix + self.name)
        for f in self.files.values():
            print("-" + prefix + "   " + f.name, f.size)
        for d in self.dirs.values():
            d.print_tree(prefix + "   ")

    def refresh_sizes(self) -> int:
        size = 0
        for f in self.files.values():
            size += f.size
        for d in self.dirs.values():
            size += d.refresh_sizes()
        self.size = size
        return size
        
class File:
    def __init__(self, size, name) -> None:
        self.size = size
        self.name = name

#Read
with open("day7input.txt") as f:
    data = [x.strip() for x in f.readlines()]
#Construct file system
root = Directory(None, "/")
current_dir = root
for line in data:
    if line.startswith('$'):
        line = line.split(" ")
        if line[1] == "cd":
            if line[2] == "..":
                current_dir = current_dir.parent
            elif line[2] == "/":
                while current_dir.parent != None:
                    current_dir = current_dir.parent
            else:
                if line[2] not in current_dir.dirs.keys():
                    current_dir.dirs[line[2]] = Directory(current_dir, line[2])
                current_dir = current_dir.dirs[line[2]]
        elif line[1] == "ls":
            pass
    elif line.startswith("dir"):
        line = line.split(" ")
        if line[1] not in current_dir.dirs.keys():
            current_dir.dirs[line[1]] = Directory(current_dir, line[1])
    else:
        line = line.split(" ")
        if line[1] not in current_dir.files.keys():
            size = int(line[0])
            current_dir.files[line[1]] = File(size, line[1])
        
#Part one
ans = 0
root.refresh_sizes()
q = deque()
q.append(root)
while q:
    curr = q.pop()
    if curr.size <= 100000:
        ans += curr.size
    q.extend(curr.dirs.values())
print("The first answer is: ", ans)

#Part two
free_space = 70000000 - root.size
needed_space = 30000000 - free_space
ans = root.size
q = deque()
q.append(root)
while q:
    curr = q.pop()
    if curr.size >= needed_space and curr.size < ans:
        ans = curr.size
    q.extend(curr.dirs.values()) 
print("The second answer is: ", ans)