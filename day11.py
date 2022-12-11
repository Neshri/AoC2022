import time
from collections import deque
t = time.perf_counter()


class Monkey:

    def __init__(self, m_id, items, operation, test, true_throw, false_throw, worry_decrease) -> None:
        self.m_id = m_id
        self.items = deque(items)
        self.operation = operation
        self.test = test
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspection_counter = 0
        self.worry_decrease = worry_decrease

    def inspect_items(self):
        global monkey_product
        for i in range(len(self.items)):
            self.items[i] = self.operation(self.items[i])
            if self.worry_decrease:
                self.items[i] = self.items[i] // 3
            self.items[i] = self.items[i] % monkey_product
            self.inspection_counter += 1

    def throw_items(self, monkeys):
        while self.items:
            if self.test(self.items[0]):
                throw_to = self.true_throw
            else:
                throw_to = self.false_throw
            monkeys[throw_to].catch_item(self.items.popleft())

    def catch_item(self, item):
        self.items.append(item)


with open("day11input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
monkey_product = 1
starting_items = []
# Part one
i = 0
monkeys = []
while i < len(lines):
    # Get monkey id
    m_id = int(lines[i].split(' ')[1][:-1])
    i += 1
    # Get starting items for monkey
    items = [int(x) for x in lines[i].removeprefix(
        "Starting items: ").split(", ")]
    # Save original list of starting items
    starting_items.append([x for x in items])
    i += 1
    # Get the operation for how worried you get from this monkey handling your items
    expr = lines[i].removeprefix("Operation: new = ")
    operation = eval("lambda old: " + expr)
    i += 1
    # Get test the monkey uses to decide where to throw items
    test = int(lines[i].split(' ')[-1])
    # Update monkey_product for handling bigass numbers
    monkey_product *= test
    def test(n, test=test): return n % test == 0
    i += 1
    true_throw = int(lines[i].split(' ')[-1])
    i += 1
    false_throw = int(lines[i].split(' ')[-1])
    i += 2
    monkeys.append(Monkey(m_id, items, operation, test,
                   true_throw, false_throw, True))

# Run simulation for 20 rounds
for round in range(20):
    for m in monkeys:
        m.inspect_items()
        m.throw_items(monkeys)
inspections = [x.inspection_counter for x in monkeys]
inspections.sort(reverse=True)
print("The first level of monkey business is: ",
      inspections[0] * inspections[1])

# Part two
# Reset monkeys
for i in range(len(monkeys)):
    monkeys[i].items = deque([x for x in starting_items[i]])
    monkeys[i].inspection_counter = 0
    monkeys[i].worry_decrease = False
# Run simulation for 10000 rounds
for round in range(10000):
    for m in monkeys:
        m.inspect_items()
        m.throw_items(monkeys)
inspections = [x.inspection_counter for x in monkeys]
inspections.sort(reverse=True)
print("The second level of monkey business is: ",
      inspections[0] * inspections[1])

print("The execution time was: ", int((time.perf_counter()-t)*1000), "ms")
