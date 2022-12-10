# CPU simulation

# Initialize the X register with the value 1
x = 1

# The addx instruction takes two cycles to complete
def addx(v):
    global x
    # After two cycles, increase the value of X by v
    x += v

# The noop instruction takes one cycle to complete and has no other effect
def noop():
    pass

# Function to check the signal strength and add it to the sum if necessary
def check_signal_strength(cycle, signal_strength_sum):
    if cycle >= 20 and (cycle - 20) % 40 == 0:
        signal_strength_sum += cycle * x
    return signal_strength_sum

def draw(cycle, x, screen):
    cycle -= 1
    if x-1 <= cycle % 40 <= x+1:
        screen[cycle//len(screen[0])][cycle%40] = '#'
    

# Define the program by reading it from a file
with open("day10input.txt") as f:
    program = [line.strip() for line in f.readlines()]

# Initialize the cycle counter and the sum of signal strengths
cycle = 1
signal_strength_sum = 0
screen = []
for i in range(6):
    screen.append([' '] * 40)
draw(cycle, x, screen)
# Execute each instruction in the program
for instruction in program:
    # Increase the cycle counter by one
    cycle += 1
    # The noop instruction takes one cycle to complete
    if instruction == "noop":
        # Do nothing
        pass
    # The addx instruction takes two cycles to complete
    elif "addx" in instruction:
        # Add the current signal strength to the sum if the cycle counter is part of the series 20, 60, 100, 140, etc.
        signal_strength_sum = check_signal_strength(cycle, signal_strength_sum)
        draw(cycle, x, screen)
        # Get the value to add to X from the instruction
        value = int(instruction.split()[1])
        # Execute the addx instruction
        addx(value)
        # Increase the cycle counter by one
        cycle += 1

    # Add the current signal strength to the sum if the cycle counter is part of the series 20, 60, 100, 140, etc.
    signal_strength_sum = check_signal_strength(cycle, signal_strength_sum)
    draw(cycle, x, screen)

# Output the sum of signal strengths
print(f"Sum of signal strengths: {signal_strength_sum}")

for line in screen:
    print("".join(line))
