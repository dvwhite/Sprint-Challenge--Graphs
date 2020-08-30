import random
#import ipdb


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
