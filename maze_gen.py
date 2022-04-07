import copy
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
            self.barrier = True
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
        self.rooms = {}
        self.passages = {}

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
     
        for room in self.rooms[self.current_level]:
            for row in range(0, self.size):
                if row >= room.y_min and row <= room.y_max:
                    for cell in range(room.x_min, room.x_max+1):
                        current_layout[row][cell] = Block('Room')

        for passage in self.passages[self.current_level]:
            for x in range(0, len(passage.x_seq)):
                current_layout[passage.y_seq[x]][passage.x_seq[x]] = Block('Room')
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
            if not self.rooms:
                self.rooms[0] = []
                self.rooms[0].append(new_room)       
            else:
                room_added = False
                for level in range(0, len(self.rooms.keys())):
                    room_conflict = None
                    for room in range(0, len(self.rooms[level])):
                        existing_x_bound = [x for x in range(self.rooms[level][room].x_min, self.rooms[level][room].x_max+1)]
                        existing_y_bound = [x for x in range(self.rooms[level][room].y_min, self.rooms[level][room].y_max+1)]
                        x_test = [x for x in new_x_bound if x in existing_x_bound]
                        y_test = [x for x in new_y_bound if x in existing_y_bound]
                        if not x_test or not y_test:
                            continue
                        else:
                            room_conflict = room
                            break
                    if room_conflict is None:
                        self.rooms[level].append(new_room)
                        room_added = True
                        break
                # If no spot is found for the room, make a new level
                if not room_added:
                    last_level = list(self.rooms.keys())[-1]
                    if room_conflict is None:
                        self.rooms[last_level].append(new_room)
                    else:
                        self.rooms[last_level+1] = []
                        self.rooms[last_level+1].append(new_room)

        
    def create_passages(self):
        for level in range(0, len(self.rooms)):
            self.passages[level] = []
            unconnected_rooms = []
            for room in self.rooms[level]:
                unconnected_rooms.append(room)
            room_from = None
            print(unconnected_rooms)
            if len(unconnected_rooms) > 1:
                while len(unconnected_rooms) > 0:
                    if not room_from:
                        room_from = unconnected_rooms.pop()
                    room_to = unconnected_rooms.pop()
                    self.passages[level].append(Passage((room_from.x_min, room_from.y_min), (room_to.x_min, room_to.y_min)))
                    room_from = room_to
                
                     
class Room:

    def __init__(self, length, x_min, y_min):
        self.side_length = length
        self.x_min = x_min
        self.x_max = self.x_min + self.side_length
        self.y_min = y_min
        self.y_max = self.y_min + self.side_length

class Passage:

    def __init__(self, start_coords, end_coords):
        self.start_x = start_coords[0]
        self.start_y = start_coords[1]
        self.end_x = end_coords[0]
        self.end_y = end_coords[1]
        self.x_seq = []
        self.y_seq = []        

        y_diff = self.start_y - self.end_y
        if y_diff != 0:
            y_sign = int(y_diff / abs(y_diff))
        x_diff = self.start_x - self.end_x
        if x_diff != 0:
            x_sign = int(x_diff / abs(x_diff))

        x_magnitude = abs(x_diff)
        y_magnitude = abs(y_diff)

        x_position = self.start_x
        while x_magnitude > 0:
            self.x_seq.append(x_position)
            self.y_seq.append(self.start_y)
            x_magnitude = x_magnitude - 1
            x_position = x_position - 1 * (x_sign)
   
        y_position = self.start_y
        while y_magnitude > 0:
            self.y_seq.append(y_position)
            self.x_seq.append(self.end_x)
            y_magnitude = y_magnitude - 1
            y_position = y_position - 1 * (y_sign)


class Player:
    
    def __init__(self):
        self.symbol = 'O'
        self.x_coord = None
        self.y_coord = None


if __name__ == "__main__":

    final_maze = Maze(30)
    final_maze.create_rooms()
    final_maze.create_passages()
    final_maze.current_level = 0

    player_1 = Player()
    print(final_maze.rooms)

    playing = True
    initialize_player = True
    while playing:
        
        os.system('clear')

        current_layout = final_maze.get_layout()
        
        # Start player in room
        while initialize_player:
            for row in range(0, len(current_layout)):
                for item in range(0, len(current_layout[row])):
                    if current_layout[row][item].symbol == '#':
                        player_1.x_coord = item
                        player_1.y_coord = row
                        initialize_player = False
                        
                
        
        # Print board                
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
                if not current_layout[player_1.y_coord-1][player_1.x_coord].barrier:
                    player_1.y_coord = player_1.y_coord - 1 
        elif x == 's':
            if player_1.y_coord < final_maze.size:
                if not current_layout[player_1.y_coord+1][player_1.x_coord].barrier:
                    player_1.y_coord += 1
        elif x == 'a':
            if player_1.x_coord > 0:
                if not current_layout[player_1.y_coord][player_1.x_coord-1].barrier:
                    player_1.x_coord = player_1.x_coord - 1
        elif x == 'd':
            if player_1.x_coord < final_maze.size:
                if not current_layout[player_1.y_coord][player_1.x_coord+1].barrier:
                    player_1.x_coord += 1
        elif x == 'q':
            break
        elif x == 'o':
            if final_maze.current_level < len(final_maze.rooms) - 1:
                final_maze.current_level += 1
        elif x == 'p':
            if final_maze.current_level > 0:
                final_maze.current_level = final_maze.current_level - 1
   
