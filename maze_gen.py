import random
import math

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

        if self.unit_type == ' ':
            self.barrier = False
            self.symbol = None

class Maze:

    def __init__(self, size):
        self.size = size
        self.levels = {}        
    
    def create_rooms(self):

        room_number = random.randrange(3, 20)
        room_upper_limit = math.floor(self.size / 3)

        for room in range(0, room_number):
            room_len = random.randrange(3, room_upper_limit)
            room_upper_left_coord_min = 1
            room_upper_left_coord_max = self.size - 1 - room_len
            room_upper_left_x = random.randrange(room_upper_left_coord_min, room_upper_left_coord_max)
            room_upper_left_y = random.randrange(room_upper_left_coord_min, room_upper_left_coord_max)
            room_lower_right_x = room_upper_left_x + room_len - 1
            room_lower_right_y = room_upper_left_y + room_len - 1
            self.assign_room_level(room_upper_left_x, room_upper_left_y, room_lower_right_x, room_lower_right_y)

    def assign_room_level(self, room_upper_left_x, room_upper_left_y, room_lower_right_x, room_lower_right_y):
        new_room_coords = (room_upper_left_x, room_upper_left_y, room_lower_right_x, room_lower_right_y)
        new_x_bound = [x for x in range(room_upper_left_x, room_lower_right_x+1)]
        new_y_bound = [x for x in range(room_upper_left_y, room_lower_right_y+1)]
        if not self.levels:
            self.levels[0] = {}
            self.levels[0]['rooms'] = [new_room_coords]       
            return
        else:
            for level in range(0, len(self.levels.keys())):
                error = False
                for room in self.levels[level]['rooms']:
                    existing_x_bound = [x for x in range(room[0], room[2]+1)]
                    existing_y_bound = [x for x in range(room[1], room[3]+1)]
                    x_test = [True for x in new_x_bound if x in existing_x_bound]
                    y_test = [True for x in new_y_bound if x in existing_y_bound]
                    if not x_test or not y_test:
                        continue
                    else:
                        error = True
                        break
                if not error:
                    self.levels[level]['rooms'].append(new_room_coords)
                    return
            # If no spot is found for the room, make a new level
            total_levels = list(self.levels.keys())
            last_level = total_levels[-1]
            if not error:
                self.levels[last_level]['rooms'].append(new_room_coords)
                return
            else:
                self.levels[last_level+1] = {}
                self.levels[last_level+1]['rooms'] = [new_room_coords]
                return       

    def build_levels(self):
        for level_number in range(0, len(self.levels.keys())):
            self.levels[level_number]['layout'] = []
            for n in range(0, self.size):
                if n == 0 or n == self.size-1:
                    top_bottom = [Block('Wall') for x in range(0, self.size)]
                    self.levels[level_number]['layout'].append(top_bottom)
                else:
                    middle = []
                    middle.append(Block('Wall'))
                    for x in range(1, self.size-1):
                        middle.append(Block('Floor'))
                    middle.append(Block('Wall'))
                    self.levels[level_number]['layout'].append(middle)
         
            for room in self.levels[level_number]['rooms']:
                for row in range(0, self.size):
                    if row >= room[1] and row <= room[3]:
                        for cell in range(room[0], room[2]+1):
                            self.levels[level_number]['layout'][row][cell] = Block('Room') 

if __name__ == "__main__":

    final_maze = Maze(30)
    final_maze.create_rooms()
    final_maze.build_levels()

    for level_number in range(0, len(final_maze.levels.keys())):
        for row in final_maze.levels[level_number]['layout']:
            for item in row:
                print(item.symbol, end='  ')
            print()
    
