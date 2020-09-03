import random
# import ipdb


def bfs_unexplored(starting_node, explored):
    # Exhaust that path
    visited = []
    nodes = [([], starting_node)]
    while nodes:
        # Get the next room in the rooms list
        (path, node) = nodes.pop()

        # Check that room's exits in the explored dict for unexplored rooms,
        # which are indicated by a '?'
        if node and node not in visited:
            exits = node.get_exits()
            if '?' in explored[node.id].values():
                for direction, dest in explored[node.id].items():
                    if dest == '?':
                        return path
            else:
                # Add node to the visited node arr
                visited.append(node)

                for ex in exits:
                    # enqueue the exits
                    nodes = [
                        (path + [ex], node.get_room_in_direction(ex))] + nodes


def bfs_unexplored_quad(starting_node, explored, world):
    """Generate a BFS path to unexplored but preferring nodes in
    the same quadrant"""

    # Get the original quadrant
    orig_quad = get_quadrant(starting_node, world)

    # Exhaust that path
    visited = []
    nodes = [([], starting_node)]
    while nodes:
        # Get the next room in the rooms list
        (path, node) = nodes.pop()

        # Check that room's exits in the explored dict for unexplored rooms,
        # which are indicated by a '?'
        if node and node not in visited:
            node_quad = get_quadrant(node, world)
            exits = node.get_exits()
            if '?' in explored[node.id].values():
                for direction, dest in explored[node.id].items():
                    if dest == '?' and node_quad == orig_quad:
                        return path
            else:
                # Add node to the visited node arr
                visited.append(node)

                for ex in exits:
                    # enqueue the exits
                    nodes = [
                        (path + [ex], node.get_room_in_direction(ex))] + nodes


def traverse_map(starting_vertex, path):
    # Traverse the map
    # Compile the path throught the map in path

    # Setup
    explored = {}
    reverse_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    curr_room = starting_vertex
    explored[curr_room.id] = {ex: '?' for ex in curr_room.get_exits()}

    # Pick a random starting direction
    rooms_to_visit = []
    rooms_to_visit.append(random.choice(curr_room.get_exits()))

    # Keep walking until you hit a dead end
    # ipdb.set_trace()
    while rooms_to_visit:
        # Reset variables
        unexplored = []

        # Get the next room
        prev_room = curr_room
        next_room_dir = rooms_to_visit.pop()

        # Explore the next room using graph
        path.append(next_room_dir)
        curr_room = curr_room.get_room_in_direction(next_room_dir)
        curr_exits = curr_room.get_exits()

        # Mark it as visited and create a new dict
        explored[prev_room.id][next_room_dir] = curr_room.id
        if curr_room.id not in explored:
            explored[curr_room.id] = {ex: '?' for ex in curr_exits}

        # Mark the room number of the opposite direction we came from as
        # visited, as long as curr_rm connects back to it
        reverse_dir = reverse_dirs[next_room_dir]
        if reverse_dir in curr_exits:
            explored[curr_room.id][reverse_dir] = prev_room.id

        # Add all unexplored exits from the current room
        unexplored = [ex for ex in explored[curr_room.id]
                      if explored[curr_room.id][ex] == '?']

        # If there's more rooms to explore, continue exploring them
        if len(unexplored) > 0:
            choice = random.choice(unexplored)
            rooms_to_visit += [choice]

        # Once the player hits a dead end, BFS to locate a path
        # back to closest unexplored location
        # Exhaust that path
        # Repeat until all paths are explored
        else:
            path_to_unexplored = bfs_unexplored(curr_room, explored)
            if not path_to_unexplored is None:
                for direction in path_to_unexplored:
                    path.append(direction)
                    curr_room = curr_room.get_room_in_direction(direction)

                # Add all unexplored exits from the current room
                unexplored = [ex for ex in explored[curr_room.id]
                              if explored[curr_room.id][ex] == '?']

                # If there's more rooms to explore, continue exploring them
                if len(unexplored) > 0:
                    choice = random.choice(unexplored)
                    rooms_to_visit += [choice]


def get_quadrant(node, world):
    """Return the quadrant of the node in world's node grid"""

    # Determine grid size
    grid_rows = len(world.room_grid)
    grid_cols = len(world.room_grid[0])
    quad = (grid_rows // 2, grid_cols // 2)

    # Split the grid of nodes into quadrants
    # [
    #   -----------
    #   | q1 | q2 |
    #   |----o----|
    #   | q3 | q4 |
    #   -----------
    # ]
    q1_rooms = [rm for row in world.room_grid[:quad[0]]
                for rm in row[:quad[1]]]
    q2_rooms = [rm for row in world.room_grid[:quad[0]:]
                for rm in row[quad[1]:]]
    q3_rooms = [rm for row in world.room_grid[quad[0]:]
                for rm in row[:quad[1]]]
    q4_rooms = [rm for row in world.room_grid[quad[0]:]
                for rm in row[quad[1]:]]

    # Determine the quadrant
    if node in q1_rooms:
        return "q1"
    elif node in q2_rooms:
        return "q2"
    elif node in q3_rooms:
        return "q3"
    elif node in q4_rooms:
        return "q4"
    else:
        raise ValueError(
            f"Error! Node with id {node.id} was not found in a quadrant")


def monte_carlo_paths(args, n_trials, results):
    [starting_vertex, path] = [*args]
    for idx in range(n_trials):
        seed_num = idx * random.randint(100, 10000)
        #seed_num = 888420
        random.seed(seed_num)
        traverse_map(starting_vertex, path)
        results.append((seed_num, path.copy()))
        path.clear()
    return results
