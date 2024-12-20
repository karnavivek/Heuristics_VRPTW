import numpy as np
import random
from collections import defaultdict

# Parameters
n = 10  # number of customers
v = 5   # number of vehicles

# Inputs (from your provided data)
nodes = [0] + [i for i in range(1, n+1)] + [n+1]
X = [100, 55, 50, 24, 141, 128, 99, 21, 69, 132, 161, 100]
Y = [100, 152, 59, 36, 29, 71, 79, 165, 163, 163, 77, 100]
distance_matrix = {(i, j): np.hypot(X[i] - X[j], Y[i] - Y[j]) for i in nodes for j in nodes if i != j}
a = {0: 0, 1: 70, 2: 70, 3: 50, 4: 50, 5: 70, 6: 50, 7: 50, 8: 50, 9: 35, 10: 40, 11: 0}
b = {0: 300, 1: 140, 2: 190, 3: 180, 4: 180, 5: 190, 6: 180, 7: 180, 8: 180, 9: 260, 10: 280, 11: 300}
s = {0: 0, 1: 10, 2: 20, 3: 30, 4: 20, 5: 30, 6: 30, 7: 50, 8: 60, 9: 20, 10: 40, 11: 0}

# Initialize routes and vehicle tracking
routes = defaultdict(list)
vehicle_time = [0] * v
vehicle_position = [0] * v
unvisited = set(range(1, n+1))

# Nearest Neighbor Heuristic
for vehicle in range(v):
    current = 0  # Start at the depot
    while unvisited:
        # Find the nearest neighbor within time constraints
        nearest = None
        min_distance = float('inf')
        for neighbor in unvisited:
            travel_time = distance_matrix[current, neighbor]
            arrival_time = vehicle_time[vehicle] + travel_time
            if arrival_time >= a[neighbor] and arrival_time <= b[neighbor]:
                if travel_time < min_distance:
                    min_distance = travel_time
                    nearest = neighbor

        # If no valid neighbor is found, return to the depot
        if nearest is None:
            routes[vehicle].append(n+1)  # End at the depot
            vehicle_time[vehicle] += distance_matrix[current, n+1]
            break

        # Visit the nearest neighbor
        routes[vehicle].append(nearest)
        vehicle_time[vehicle] += distance_matrix[current, nearest] + s[nearest]
        current = nearest
        unvisited.remove(nearest)

    # Add depot at the end if it's not already there
    if routes[vehicle][-1] != n+1:
        routes[vehicle].append(n+1)

# Output the routes and total cost
total_distance = 0
for vehicle, route in routes.items():
    print(f"Vehicle {vehicle + 1} route: {route}")
    route_distance = sum(distance_matrix[route[i], route[i+1]] for i in range(len(route)-1))
    total_distance += route_distance
    print(f"Distance: {route_distance:.2f}")

print(f"Total Distance: {total_distance:.2f}")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define colors for different vehicles
colors = plt.cm.get_cmap("tab10", v)  # Get a colormap with 'v' distinct colors

# Create a plot
plt.figure(figsize=(12, 5))

# Plot the nodes
for i in nodes:
    if i == 0 or i == n+1:  # Depots
        plt.scatter(X[i], Y[i], c='red', s=200, label='Depot' if i == 0 else None, edgecolors='black')
        plt.text(X[i], Y[i], f"D", fontsize=10, ha='center', va='center', color='white')
    else:  # Customers
        plt.scatter(X[i], Y[i], c='blue', s=100, edgecolors='black')
        plt.text(X[i], Y[i], f"{i}", fontsize=8, ha='center', va='center')

# Plot the routes
for vehicle, route in routes.items():
    route_color = colors(vehicle / v)  # Assign a color to each vehicle
    for i in range(len(route) - 1):
        start, end = route[i], route[i + 1]
        plt.plot([X[start], X[end]], [Y[start], Y[end]], c=route_color, linewidth=2, label=f'Vehicle {vehicle + 1}' if i == 0 else "")

# Add legend
handles = [
    mpatches.Patch(color=colors(i / v), label=f'Vehicle {i + 1}') for i in range(v)
]
plt.legend(handles=handles, loc='upper left', fontsize=8)

# Add title and labels
plt.title("VRPTW - Routes Visualization")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")
plt.grid(True)

# Show the plot
plt.show()
