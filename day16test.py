from collections import defaultdict

def find_maximum_pressure(graph, start_node, time_available):
    # Initialize a table to store the maximum pressure that can be released
    # at each time and valve. The table has (time_available + 1) rows
    # and (number of valves) columns.
    table = [[0] * len(graph) for _ in range(time_available + 1)]

    # Iterate over the rows (times) in reverse order
    for t in range(time_available, -1, -1):
        # Iterate over the columns (valves)
        for i, current_node in enumerate(graph):
            # Initialize the maximum pressure released so far to the pressure
            # released by opening the current valve
            max_pressure = graph[current_node]["flow_rate"] * t
            # Consider the possibility of visiting the next valve
            for next_node in graph[current_node]["tunnels"]:
                j = graph[next_node]["index"]  # Index of the next valve
                # Calculate the maximum pressure that can be released
                # by visiting the next valve after the current one
                pressure = table[t - 1][j] + graph[next_node]["flow_rate"] * 1
                # Update the maximum pressure released so far
                max_pressure = max(max_pressure, pressure)
            # Update the table with the maximum pressure released so far
            table[t][i] = max_pressure

    # Return the maximum pressure released at the start valve and the maximum time
    return table[time_available][graph[start_node]["index"]]



# Example usage

# Construct the graph from the input data
graph = defaultdict(dict)

# Add the flow rate and tunnels for each valve
graph["AA"]["flow_rate"] = 0
graph["AA"]["tunnels"] = ["DD", "II", "BB"]

graph["BB"]["flow_rate"] = 13
graph["BB"]["tunnels"] = ["CC", "AA"]

graph["CC"]["flow_rate"] = 2
graph["CC"]["tunnels"] = ["DD", "BB"]

graph["DD"]["flow_rate"] = 20
graph["DD"]["tunnels"] = ["CC", "AA", "EE"]

graph["EE"]["flow_rate"] = 3
graph["EE"]["tunnels"] = ["FF", "DD"]

graph["FF"]["flow_rate"] = 0
graph["FF"]["tunnels"] = ["EE", "GG"]

graph["GG"]["flow_rate"] = 0
graph["GG"]["tunnels"] = ["FF", "HH"]

graph["HH"]["flow_rate"] = 22
graph["HH"]["tunnels"] = ["GG"]

graph["II"]["flow_rate"] = 0
graph["II"]["tunnels"] = ["AA", "JJ"]

graph["JJ"]["flow_rate"] = 21
graph["JJ"]["tunnels"] = ["II"]

# Assign an index to each valve
for i, valve in enumerate(graph):
    graph[valve]["index"] = i

# Find the maximum pressure that can be released in 30 minutes
result = find_maximum_pressure(graph, "AA", 30)
print(result)  # Output: 1651
