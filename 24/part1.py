from copy import deepcopy
from time import sleep
import sys
sys.setrecursionlimit(1000000)

INPUT_FILE = r'input_file.txt'

class Tile:

    def __init__(self, symbol, row, column):
        self.row, self.column = row, column
        self.symbol = symbol
        self.neighbor_tiles = {
            'right' : None,
            'left' : None,
            'up' : None,
            'down' : None,
        }
        self.border = {
            'right' : False,
            'left' : False,
            'up' : False,
            'down' : False,
        }
        self.right_border = False
        self.left_border = False
        self.up_border = False
        self.down_border = False
        self.blizzard_occupants = []
        self.__is_end_tile = False
        self.__is_current_tile = False
    
    def get_key(self):
        return (self.row, self.column)
    
    def set_is_current_tile_flag(self, value):
        self.__is_current_tile = value
    
    def set_as_end_tile(self):
        self.__is_end_tile = True

    def is_end_tile(self):
        return self.__is_end_tile
    
    def set_neighbor_tile(self, tile, direction):
        self.neighbor_tiles[direction] = tile
    
    def add_blizzard_occupants(self, blizzard):
        self.blizzard_occupants.append(blizzard)
    
    def remove_blizzard_occupants(self, blizzard):
        self.blizzard_occupants.remove(blizzard)
    
    def attach_tile(self, tile, from_direction, to_direction):
        self.set_neighbor_tile(tile, from_direction)
        tile.set_neighbor_tile(self, to_direction)

    def get_next_tile(self, direction):
        return self.neighbor_tiles[direction], self.border[direction]
    
    def set_border(self, direction, border=True):
        self.border[direction] = border
    
    def get_symbol(self):
        if self.__is_current_tile:
            return 'E'
        if not self.blizzard_occupants:
            return self.symbol
        if len(self.blizzard_occupants) == 1:
            return self.blizzard_occupants[0].get_symbol()
        return f'{len(self.blizzard_occupants)}'
    
    def get_blizzard_count(self):
        return len(self.blizzard_occupants)
        

class Map:
    
    def __init__(self):
        self.corners = {
            'upper_left':None,
            'upper_right':None,
            'lower_left':None,
            'lower_right':None,
        }
        self.col_count = 0
        self.row_count = 0
        self.start_tile = None
        self.end_tile = None
        self.blizzard_list = []
    
    def add_blizzard(self, blizzard):
        self.blizzard_list.append(blizzard)
    
    def move_to_next_state(self):
        for blizzard in self.blizzard_list:
            blizzard.move_to_next_tile()

    def add_row(self, row):

        self.row_count += 1
        self.col_count = max(len(row), self.col_count)
        

        if self.corners['lower_left'] is not None:
            upper_item = self.corners['lower_left']
            for item in row:
                upper_item.attach_tile(item, 'down', 'up')
                upper_item, _ = upper_item.get_next_tile('right')

        previous_item = None
        for item in row:
            if self.corners['upper_left'] is None:
                self.corners['upper_left'] = item
            
            if previous_item is None:
                previous_item = item
                continue

            previous_item.attach_tile(item, 'right', 'left')
            previous_item = item
        
        if self.corners['upper_right'] is None:
            self.corners['upper_right'] = row[-1]
        
        self.corners['lower_left'], self.corners['lower_right'] = row[0], row[-1]
    
    def iterate_on_all_tiles(self):

        yield self.start_tile
        yield self.end_tile

        left_most_item = self.corners['upper_left']

        while True:
            current_item = left_most_item
            while True:
                yield current_item
                current_item, right_border = current_item.get_next_tile('right')
                if right_border:
                    break
            left_most_item, down_border = left_most_item.get_next_tile('down')
            if down_border:
                break
    
    def get_key(self):
        key=''
        for item in self.iterate_on_all_tiles():
            key += item.get_symbol()
        return key

    
    def print_map(self):

        left_most_item = self.corners['upper_left']

        while True:
            current_item = left_most_item
            while True:
                symbol = current_item.get_symbol()
                print(symbol, end='')
                current_item, right_border = current_item.get_next_tile('right')
                if right_border:
                    break
            print()
            left_most_item, down_border = left_most_item.get_next_tile('down')
            if down_border:
                break
    
    def add_map_borders(self):
        upper_item: Tile
        lower_item: Tile
        left_item: Tile
        right_item: Tile

        upper_item = self.corners['upper_left']
        lower_item = self.corners['lower_left']
        for _ in range(self.col_count):
            upper_item.set_border('up')
            lower_item.set_border('down')
            upper_item, _ = upper_item.get_next_tile('right')
            lower_item, _ = lower_item.get_next_tile('right')

        left_item = self.corners['upper_left']
        right_item = self.corners['upper_right']
        for _ in range(self.row_count):
            left_item.set_border('left')
            right_item.set_border('right')
            left_item, _ = left_item.get_next_tile('down')
            right_item, _ = right_item.get_next_tile('down')

    def wrap_map(self):
        upper_item = self.corners['lower_left']
        lower_item = self.corners['upper_left']
        for _ in range(self.col_count):
            upper_item.attach_tile(lower_item, 'down', 'up')
            upper_item, _ = upper_item.get_next_tile('right')
            lower_item, _ = lower_item.get_next_tile('right')

        left_item = self.corners['upper_right']
        right_item = self.corners['upper_left']
        for _ in range(self.row_count):
            left_item.attach_tile(right_item, 'right', 'left')
            left_item, _ = left_item.get_next_tile('down')
            right_item, _ = right_item.get_next_tile('down')
        

    def add_start_tile(self, tile):
        self.start_tile = tile
        self.corners['upper_left'].set_border('up', False)
        self.corners['upper_left'].attach_tile(tile, 'up', 'down')
        tile.set_border('up')
        tile.set_border('left')
        tile.set_border('right')

    def add_end_tile(self, tile):
        self.end_tile = tile
        self.corners['lower_right'].set_border('down', False)
        self.corners['lower_right'].attach_tile(tile, 'down', 'up')
        tile.set_border('down')
        tile.set_border('left')
        tile.set_border('right')


class Blzzard:
    
    def __init__(self, arrow_symbol, tile):
        self.symbol = arrow_symbol
        self.direction = {
            '>':'right',
            '<':'left',
            '^':'up',
            'v':'down',
        }[self.symbol]
        self.current_tile = tile
        self.current_tile.add_blizzard_occupants(self)

    def get_symbol(self):
        return self.symbol

    def move_to_next_tile(self):
        next_tile, _ = self.current_tile.get_next_tile(self.direction)
        self.current_tile.remove_blizzard_occupants(self)
        next_tile.add_blizzard_occupants(self)
        self.current_tile = next_tile


def iterate_input_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')

class CoorStateGraph:

    def __init__(self, map:Map,):
        self.tile_blizzard_count = []
        self.map_state_count = 0
        self.graph_neighbors = {}
        self.fill_tile_blizzard_count(map)
        print(self.map_state_count)
        self.fill_graph_neighbors(map)
        print(len(self.graph_neighbors))

    def fill_graph_neighbors(self, map):
        for state in range(self.map_state_count):
            for tile in map.iterate_on_all_tiles():
                row, col = tile.get_key()
                self.graph_neighbors[(row, col, state)] = self.get_next_states(tile, state)
    
    def fill_tile_blizzard_count(self, map:Map):
        self.tile_blizzard_count = []
        self.map_state_count = 0
        map_keys = set([])
        while True:
            key = map.get_key()
            if key in map_keys:
                break
            state_tile_blizzard_count = {tile.get_key():tile.get_blizzard_count() for tile in map.iterate_on_all_tiles()}
            self.tile_blizzard_count.append(state_tile_blizzard_count)
            map_keys.add(key)
            self.map_state_count += 1
            map.move_to_next_state()
    
    def get_next_states(self, current_tile, state):
        next_states = []

        next_tiles_info = list(map(current_tile.get_next_tile, ['right', 'left', 'down', 'up']))
        next_tiles = [tile for tile, is_border in next_tiles_info if not is_border] + [current_tile]

        for tile in next_tiles:
            next_state = (state+1)%self.map_state_count
            row, col = tile.get_key()
            if self.get_tile_blizzard_count(row, col, next_state) > 0:
                continue
            next_states.append((row, col, next_state))
        
        return next_states
    
    def get_tile_blizzard_count(self, row, col, state):
        return self.tile_blizzard_count[state][(row, col)]

    def get_graph(self):
        return self.graph_neighbors

    def print_graph(self):
        for key, value in self.graph_neighbors.items():
            print(key, value)


def get_min_distance(g, starting_node, end_coor):

    mininum_distance = float('inf')
    shortest_path = {x:float('inf') for x in g.keys()}
    shortest_path[starting_node] = 0

    visited = set([starting_node])
    queue = [starting_node]

    while queue:

        current_node = queue.pop(0)

        for neighbor_node in g[current_node]:
            # if neighbor_node in visited:
            #     continue
            shortest_path[neighbor_node] = min(shortest_path[neighbor_node], shortest_path[current_node]+1)
            row, col, _ = neighbor_node
            if (row, col) == end_coor:
                mininum_distance = min(mininum_distance, shortest_path[neighbor_node])
                print(f'mininum_distance: {mininum_distance}')
                continue
            if shortest_path[neighbor_node] > mininum_distance:
                continue
            if neighbor_node not in visited:
                visited.add(neighbor_node)
                queue.append(neighbor_node)

    return mininum_distance



def main():

    input_lines = [line for line in iterate_input_file_lines()]

    map = Map()
    for i, line in enumerate(input_lines[1:-1]):
        tile_row = []
        for j, tile in enumerate(line):
            if tile == '#':
                continue
            tile_obj = Tile('.', i+1, j+1)
            tile_row.append(tile_obj)
            if tile != '.':
                b = Blzzard(tile, tile_obj)
                map.add_blizzard(b)
        map.add_row(tile_row)

    map.wrap_map()
    map.add_map_borders()
    start_tile = Tile('.', 0, 1)
    end_tile = Tile('.', map.row_count+1, map.row_count)
    map.add_start_tile(start_tile)
    map.add_end_tile(end_tile)

    g = CoorStateGraph(map)
    starting_node = (0,1,0)
    graph = g.get_graph()
    shortest_distance = get_min_distance(graph, starting_node, end_tile.get_key())
    print(shortest_distance)

    

if __name__=='__main__':
    main()