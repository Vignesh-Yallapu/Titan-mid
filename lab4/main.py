import numpy as np
import matplotlib.pyplot as plt
import random
import math

def parse_tsp_file(filename):
    """Parses a TSP file and returns a list of city coordinates."""
    coordinates = []
    in_coordinates_section = False
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith('NODE_COORD_SECTION'):
                in_coordinates_section = True
                continue
            if in_coordinates_section and line.strip() and not line.startswith('EOF'):
                city_number, x, y = map(float, line.split())  # Changed to float for accuracy
                coordinates.append((x, y))
    return coordinates


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def total_distance(tour):
    """Calculate the total distance of a tour."""
    return sum(calculate_distance(coordinates[tour[i]], coordinates[tour[i-1]]) for i in range(len(tour)))


def generate_initial_tour():
    """Generate a random initial tour."""
    return random.sample(range(len(coordinates)), len(coordinates))


def two_opt_swap(tour):
    """Perform a 2-opt swap."""
    a, b = sorted(random.sample(range(len(tour)), 2))
    return tour[:a] + tour[a:b+1][::-1] + tour[b+1:]


def simulated_annealing(initial_temp=10000, cooling_rate=0.999, num_iterations=2000000):
    current_tour = generate_initial_tour()
    current_distance = total_distance(current_tour)
    best_tour = current_tour
    best_distance = current_distance
    temperature = initial_temp

    for i in range(num_iterations):
        neighbor_tour = two_opt_swap(current_tour)  # Using 2-opt swap instead of random swap
        neighbor_distance = total_distance(neighbor_tour)

        # Accept neighbor if it's better or based on a probability (Simulated Annealing criteria)
        if neighbor_distance < current_distance or random.random() < math.exp((current_distance - neighbor_distance) / temperature):
            current_tour = neighbor_tour
            current_distance = neighbor_distance

            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance

        # Cool down the temperature
        temperature *= cooling_rate

        # Print progress every 10,000 iterations
        if i % 10000 == 0:
            print(f"Iteration {i}, Best distance: {best_distance:.2f}, Temperature: {temperature:.2f}")

    return best_tour, best_distance


def plot_tour(tour):
    """Plot the tour on a scatter plot."""
    plt.figure(figsize=(12, 8))
    x = [coordinates[i][0] for i in tour]
    y = [coordinates[i][1] for i in tour]
    plt.plot(x + [x[0]], y + [y[0]], 'b-')  # Complete the tour by returning to the start
    plt.scatter(x, y, c='red', s=20)
    for i, (x, y) in enumerate(coordinates):
        plt.annotate(str(i + 1), (x, y), xytext=(5, 5), textcoords='offset points')
    plt.title("Optimized Tour for Bonn VLSI Dataset")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(True)
    plt.show()


# Specify the TSP file path
tsp_file = "t1.tsp"  # Replace with your actual file name

# Read coordinates from the file
coordinates = parse_tsp_file(tsp_file)

# Run the simulated annealing algorithm
best_tour, best_distance = simulated_annealing()

print("\nBest tour found:")
print(" -> ".join(str(i + 1) for i in best_tour))
print(f"\nTotal distance: {best_distance:.2f}")

# Plot the best tour
plot_tour(best_tour)
