import math
import os
import random

class Block:

    def __init__(self, unit_type = None):
        
        self.unit_type = unit_type
        self.barrier = None
        self.symbol = None

        if self.unit_type == 'Wall':
            self.barrier = True
            self.symbol = 'X'

        if self.unit_type == 'Floor':
            self.barrier = False
            self.symbol = '-'

        if self.unit_type == 'Room':
            self.barrier = False
            self.symbol = '#'

        if self.unit_type == 'Up':
            self.barrier = False
            self.symbol = 'U'

        if self.unit_type == 'Down':
            self.barrier = False
            self.symbol = 'D' 


class Maze:

    def __init__(self, size):
        self.size = size
        self.current_level = None
        self.levels = {}

    # Render current layout
    def get_layout(self):
        current_layout = []
        for n in range(0, self.size):
            if n == 0 or n == self.size-1:
                top_bottom = [Block('Wall') for x in range(0, self.size)]
                current_layout.append(top_bottom)
            else:
                middle = []
                middle.append(Block('Wall'))
                for x in range(1, self.size-1):
                    middle.append(Block('Floor'))
                middle.append(Block('Wall'))
                current_layout.append(middle)
     
        for room in self.levels[self.current_level]:
            for row in range(0, self.size):
                if row >= room.y_min and row <= room.y_max:
                    for cell in range(room.x_min, room.x_max+1):
                        current_layout[row][cell] = Block('Room')
        return current_layout
    
    def create_rooms(self):

        room_number = random.randrange(3, 20)
        room_upper_limit = math.floor(self.size / 3)

        for room in range(0, room_number):
            room_len = random.randrange(3, room_upper_limit)
            room_coord_bound_min = 1
            room_coord_bound_max = self.size - 1 - room_len
            room_x_min = random.randrange(room_coord_bound_min, room_coord_bound_max)
            room_y_min = random.randrange(room_coord_bound_min, room_coord_bound_max)
            
            new_room = Room(room_len, room_x_min, room_y_min)

            # Assign room
            new_x_bound = [x for x in range(new_room.x_min, new_room.x_max+1)]
            new_y_bound = [x for x in range(new_room.y_min, new_room.y_max+1)]
            if not self.levels:
                self.levels[0] = []
                self.levels[0].append(new_room)       
            else:
                room_added = False
                for level in range(0, len(self.levels.keys())):
                    room_conflict = None
                    for room in range(0, len(self.levels[level])):
                        existing_x_bound = [x for x in range(self.levels[level][room].x_min, self.levels[level][room].x_max+1)]
                        existing_y_bound = [x for x in range(self.levels[level][room].y_min, self.levels[level][room].y_max+1)]
                        x_test = [x for x in new_x_bound if x in existing_x_bound]
                        y_test = [x for x in new_y_bound if x in existing_y_bound]
                        if not x_test or not y_test:
                            continue
                        else:
                            room_conflict = room
                            break
                    if room_conflict is None:
                        self.levels[level].append(new_room)
                        room_added = True
                        break
                # If no spot is found for the room, make a new level
                if not room_added:
                    last_level = list(self.levels.keys())[-1]
                    if room_conflict is None:
                        self.levels[last_level].append(new_room)
                    else:
                        self.levels[last_level+1] = []
                        self.levels[last_level+1].append(new_room)

class Room:

    def __init__(self, length, x_min, y_min):
        self.side_length = length
        self.x_min = x_min
        self.x_max = self.x_min + self.side_length
        self.y_min = y_min
        self.y_max = self.y_min + self.side_length


class Player:
    
    def __init__(self):
        self.symbol = 'O'
        self.x_coord = 15
        self.y_coord = 15


if __name__ == "__main__":

    final_maze = Maze(60)
    final_maze.create_rooms()
    final_maze.current_level = 0

    player_1 = Player()
    print(final_maze.levels)

    playing = True
    while playing:
        
        os.system('clear')

        current_layout = final_maze.get_layout()
        for row in range(0, len(current_layout)):
            for item in range(0, len(current_layout[row])):
                if row == player_1.y_coord and item == player_1.x_coord:
                    print(player_1.symbol, end= ' ')
                else:
                    print(current_layout[row][item].symbol, end=' ')
            print()

        x = input()
        if x == 'w':
            if player_1.y_coord > 0:
                player_1.y_coord = player_1.y_coord - 1 
        elif x == 's':
            if player_1.y_coord < final_maze.size:
                player_1.y_coord += 1
        elif x == 'a':
            if player_1.x_coord > 0:
                player_1.x_coord = player_1.x_coord - 1
        elif x == 'd':
            if player_1.x_coord < final_maze.size:
                player_1.x_coord += 1
        elif x == 'q':
            break
        elif x == 'o':
            if final_maze.current_level < len(final_maze.levels) - 1:
                final_maze.current_level += 1
        elif x == 'p':
            if final_maze.current_level > 0:
                final_maze.current_level = final_maze.current_level - 1
    
