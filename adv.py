from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from utils import bfs_unexplored
#import ipdb

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Traverse the maze
# Compile the path throught the maxe in traversal_path

# Setup
explored = {}
reverse_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
curr_room = player.current_room
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

    # Travel there
    #print("Moving player", next_room_dir)
    player.travel(next_room_dir)
    traversal_path.append(next_room_dir)
    curr_room = player.current_room
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
    unexplored = [ex for (ex, room_id)
                  in explored[curr_room.id].items() if room_id == '?']

    # If there's more rooms to explore, continue exploring them
    if len(unexplored) > 0:
        rooms_to_visit += [random.choice(unexplored)]

    # Once the player hits a dead end, BFS to locate a path
    # back to closest unexplored location
    # Exhaust that path
    # Repeat until all paths are explored
    else:
        path_to_unexplored = bfs_unexplored(curr_room, explored)
        if not path_to_unexplored is None:
            for direction in path_to_unexplored:
                player.travel(direction)
                traversal_path.append(direction)
                # print("Backtracking " + direction + "...")

            # Add all unexplored exits from the current room
            curr_room = player.current_room
            unexplored = [ex for (ex, room_id)
                          in explored[curr_room.id].items() if room_id == '?']

            # If there's more rooms to explore, continue exploring them
            if len(unexplored) > 0:
                rooms_to_visit += [random.choice(unexplored)]

# print(traversal_path)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
