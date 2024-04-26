# utils.py
import base64
import json
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, grid, obstacle_data):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < grid[0] and 0 <= neighbor[1] < grid[1]:
                if is_obstacle(neighbor[0], neighbor[1], obstacle_data):
                    continue
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return []


def create_grid(width, height):
    return [(x, y) for x in range(width) for y in range(height)]

def is_within_sight(x1, y1, x2, y2, sight_distance):
    return max(abs(x1 - x2), abs(y1 - y2)) <= sight_distance

def calculate_item_direction_and_distance(start, goal, grid_size, obstacle_data):
    path = astar(start, goal, grid_size, obstacle_data)
    if path and len(path) > 1:
        first_step = path[1]
        dx, dy = first_step[0] - start[0], first_step[1] - start[1]
        direction, _ = get_direction_from_deltas(dx, dy)
        distance = 1
        for i in range(2, len(path)):
            next_dx, next_dy = path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]
            next_direction, _ = get_direction_from_deltas(next_dx, next_dy)
            if next_direction == direction:
                distance += 1
            else:
                break
        total_distance = len(path) - 1  # Calculate the total distance as the number of steps in the path
        return direction, distance, total_distance
    return None, None, None

def get_possible_movements(x, y, max_distance=5, grid_size=32, obstacle_data=None, destinations=None):
    if obstacle_data is None:
        obstacle_data = []
    if destinations is None:
        destinations = []
    print(f"Obstacle data at start of function: {obstacle_data}")  # Debugging statement
    directions = {
        'N': (0, -1), 'NE': (1, -1), 'E': (1, 0), 'SE': (1, 1),
        'S': (0, 1), 'SW': (-1, 1), 'W': (-1, 0), 'NW': (-1, -1)
    }
    possible_movements = {}
    for direction, (dx, dy) in directions.items():
        for distance in range(1, max_distance + 1):
            new_x, new_y = x + dx * distance, y + dy * distance
            print(f"Checking direction: {direction}, distance: {distance}, new_x: {new_x}, new_y: {new_y}")
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if is_obstacle(new_x, new_y, obstacle_data):
                    possible_movements[direction] = distance - 1
                    break
                else:
                    possible_movements[direction] = distance
            else:
                break
        else:
            possible_movements[direction] = max_distance

    destination_direction = {}
    for dest_name, (dest_x, dest_y) in destinations.items():
        path = astar((x, y), (dest_x, dest_y), (grid_size, grid_size), obstacle_data)
        if path and len(path) > 1:
            next_step = path[1]
            dx, dy = next_step[0] - x, next_step[1] - y
            direction, _ = get_direction_from_deltas(dx, dy)
            distance = 1
            for i in range(2, len(path)):
                next_dx, next_dy = path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]
                next_direction, _ = get_direction_from_deltas(next_dx, next_dy)
                if next_direction == direction and distance < max_distance:
                    distance += 1
                else:
                    break
            destination_direction[dest_name] = {direction: min(distance, max_distance)}
        else:
            print(f"No valid path found to destination {dest_name}")

    return possible_movements, destination_direction

def load_obstacle_layer(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        for layer in data['layers']:
            if layer['name'] == 'obstacle' and layer['encoding'] == 'base64':  # Corrected the layer name
                print("Found the obstacle layer.")
                decoded_data = base64.b64decode(layer['data'])
                # Assuming the data is stored as 32-bit integers (common in Tiled for tile layers)
                obstacle_data = [decoded_data[i] for i in range(0, len(decoded_data), 4)]
                print(f"Obstacle data length: {len(obstacle_data)}")
                return obstacle_data
    return []

def is_obstacle(x, y, obstacle_data, width=32):
    index = y * width + x
    if index < 0 or index >= len(obstacle_data):
        print(f"Index out of range: {index}, Data Length: {len(obstacle_data)}")
        return False
    #print(f"Checking obstacle at index {index}: {obstacle_data[index]}")
    return obstacle_data[index] != 0

def get_direction_from_deltas(dx, dy):
    if dy < 0:  # North
        if dx < 0:
            return 'NW', max(abs(dx), abs(dy))
        elif dx > 0:
            return 'NE', max(abs(dx), abs(dy))
        else:
            return 'N', abs(dy)
    elif dy > 0:  # South
        if dx < 0:
            return 'SW', max(abs(dx), abs(dy))
        elif dx > 0:
            return 'SE', max(abs(dx), abs(dy))
        else:
            return 'S', abs(dy)
    else:  # East or West
        if dx < 0:
            return 'W', abs(dx)
        elif dx > 0:
            return 'E', abs(dx)
    return 'Here', 0  # Same position

# Example usage
if __name__ == "__main__":
    obstacle_data = load_obstacle_layer('dungeon.json')
    # Test specific coordinates
    test_coords = [(15, 15), (18, 12)]
    for x, y in test_coords:
        is_obst = is_obstacle(x, y, obstacle_data)
        print(f"Is there an obstacle at ({x}, {y})? {'Yes' if is_obst else 'No'}")