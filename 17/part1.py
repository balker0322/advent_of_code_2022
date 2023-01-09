INPUT_FILE = r'input.txt'
import time


class Rock:

    def __init__(self):
        self.rock_layers = []
        self.rock_width = 0
    
    def add_layer(self, layer):
        layer = [1 if x=='#' else 0 for x in list(layer)]
        self.rock_width = len(layer)
        self.rock_layers.append(layer)

    def print_rock(self):
        for layer in self.rock_layers:
            print(layer)

class RockSource:

    def __init__(self):
        self.rock_types = []
        self.rock_type_count = 0
        self.next_rock_index = 0

    def add_rock_type(self, rock:Rock):
        self.rock_types.append(rock)
        self.rock_type_count += 1

    def get_next_rock(self):
        next_rock = self.rock_types[self.next_rock_index]
        self.next_rock_index = (self.next_rock_index+1)%self.rock_type_count
        return next_rock

class Wind:

    def __init__(self, raw_input):
        self.wind_directions = [1 if x=='>' else -1 for x in list(raw_input)]
        self.wind_direction_count = len(self.wind_directions)
        self.next_wind_direction_index = 0
        
    def get_next_direction(self):
        next_direction = self.wind_directions[self.next_wind_direction_index]
        self.next_wind_direction_index = (self.next_wind_direction_index+1)%self.wind_direction_count
        return next_direction

class Tower:

    def __init__(self, rock_source:RockSource, wind_source:Wind):
        self.rock_source = rock_source
        self.wind_source = wind_source
        self.rock_height = 0
        self.tower = []
        self.tower_width = 7
        self.rock_gap_from_left_default = 2
        self.initial_rock_gap = 3
        self.empty_layer = [1]+[0 for _ in range(self.tower_width)]+[1]
        self.bottom_layer = [1]+[1 for _ in range(self.tower_width)]+[1]

        self.add_bottom_layer()
        self.add_empty_layer()
        self.add_empty_layer()
        self.add_empty_layer()
    
    def add_bottom_layer(self):
        self.tower.append(self.bottom_layer)
    
    def add_empty_layer(self):
        self.tower.append(self.empty_layer)

    def initialize_rock_layers(self, rock_layers):
        new_rock_layers = []
        for layer in rock_layers:
            layer_width = len(layer)
            new_layer = [0 for _ in range(self.rock_gap_from_left_default+1)]+layer+[0 for _ in range(self.tower_width - layer_width-1)]
            new_rock_layers.append(new_layer)
        return new_rock_layers

    def move_rock_layers_sideway(self, rock_layers, direction):
        new_rock_layers = []
        for layer in rock_layers:
            new_layer = list(layer)
            if direction == 1:
                new_layer.pop()
                new_layer = [0] + new_layer
                new_rock_layers.append(new_layer)
                continue
            new_layer = new_layer[1:] + [0]
            new_rock_layers.append(new_layer)
        return new_rock_layers
    
    def add_layers(self, layer1, layer2):
        return [layer1[i]+layer2[i] for i in range(self.tower_width+2)]
    
    def is_collision_detected(self, bottom_comparison_index, temp_rock_layers):

        for row, rock_layer in enumerate(temp_rock_layers):
            comparison_index = bottom_comparison_index + row

            while comparison_index > len(self.tower) - 1:
                self.add_empty_layer()

            if 2 in self.add_layers(self.tower[comparison_index], rock_layer):
                return True

        return False

    def merge_rock_to_tower(self, starting_index, rock_layers):
        for i, rock_layer in enumerate(rock_layers):
            tower_index = starting_index + i
            ans = self.add_layers(self.tower[tower_index], rock_layer)
            if 2 in ans:
                pass
            self.tower[tower_index] = self.add_layers(self.tower[tower_index], rock_layer)
    
    def add_rock(self):
        next_rock_layers = list(self.rock_source.get_next_rock().rock_layers)
        next_rock_layers.reverse()
        current_rock_layers = self.initialize_rock_layers(next_rock_layers)

        # for layer in current_rock_layers:
        #     print(layer)

        bottom_comparison_index = self.rock_height + self.initial_rock_gap + 1

        print_active = False
        # if self.rock_height > 40:
        #     print_active = True

        while True:

            # pushed by jet
            temp_rock_layers = self.move_rock_layers_sideway(current_rock_layers, self.wind_source.get_next_direction())
            is_collision_detected = self.is_collision_detected(bottom_comparison_index, temp_rock_layers)
            if not is_collision_detected:
                current_rock_layers = temp_rock_layers
            
            if print_active: self.print_tower_with_falling(current_rock_layers, bottom_comparison_index)

            # fall by one unit
            temp_index = bottom_comparison_index - 1
            is_collision_detected = self.is_collision_detected(temp_index, current_rock_layers)

            if is_collision_detected:
                self.merge_rock_to_tower(bottom_comparison_index, current_rock_layers)
                self.rock_height = max(temp_index + len(current_rock_layers), self.rock_height)
                break
            
            bottom_comparison_index = temp_index

            if print_active: self.print_tower_with_falling(current_rock_layers, bottom_comparison_index)
        
        if print_active: self.print_tower()

    def print_tower_with_falling(self, rock_layers, tower_index):
        time.sleep(1)
        for _ in range(10):
            print()
        temp_list = [['#' if x==1 else '.' for x in row] for row in self.tower]
        for i, layer in enumerate(rock_layers):
            new_layer = ['O' if layer[x]==1 else temp_list[tower_index+i][x] for x in range(len(layer))]
            temp_list[tower_index+i] = new_layer
        
        temp_list = [['|'] + row[1:-1] + ['|'] for row in temp_list]
        temp_list = [''.join(row)+f' {i}' for i, row in enumerate(temp_list)]
        temp_list.reverse()
        temp_list = temp_list[:min(20, len(temp_list))]
        for row in temp_list:
            print(row)
        print(self.rock_height)
        

    def print_tower(self):
        time.sleep(1)
        for _ in range(10):
            print()
        temp_list = [['#' if x==1 else '.' for x in row] for row in self.tower]
        temp_list = [['|'] + row[1:-1] + ['|'] for row in temp_list]
        temp_list = [''.join(row)+f' {i}' for i, row in enumerate(temp_list)]
        temp_list.reverse()
        temp_list = temp_list[:min(20, len(temp_list))]
        for row in temp_list:
            print(row)
        print(self.rock_height)


def get_file_line(input_file=INPUT_FILE):
    with open(input_file, 'r') as f:
        for line in f:
            return line.strip()

def initialize_rock_source() -> RockSource:

    rock_source = RockSource()

    rock1 = Rock()
    rock1.add_layer('####')
    rock_source.add_rock_type(rock1)

    rock2 = Rock()
    rock2.add_layer('.#.')
    rock2.add_layer('###')
    rock2.add_layer('.#.')
    rock_source.add_rock_type(rock2)

    rock3 = Rock()
    rock3.add_layer('..#')
    rock3.add_layer('..#')
    rock3.add_layer('###')
    rock_source.add_rock_type(rock3)

    rock4 = Rock()
    rock4.add_layer('#')
    rock4.add_layer('#')
    rock4.add_layer('#')
    rock4.add_layer('#')
    rock_source.add_rock_type(rock4)

    rock5 = Rock()
    rock5.add_layer('##')
    rock5.add_layer('##')
    rock_source.add_rock_type(rock5)

    return rock_source

def main():
    rock_source = initialize_rock_source()
    wind_source = Wind(get_file_line())
    tower = Tower(rock_source, wind_source)
    for _ in range(2022):
        tower.add_rock()
    tower.print_tower()
    print(tower.rock_height)

if __name__=='__main__':
    main()