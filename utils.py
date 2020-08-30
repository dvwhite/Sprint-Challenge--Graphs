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
