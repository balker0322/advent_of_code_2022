from dataclasses import dataclass

INPUT_FILE = r'input_file.txt'

@dataclass
class Tile:
    row:int
    column:int
    tile_type:str
    left = None
    right = None
    up = None
    down = None

    def get_next_tile(self, face, step):
        next_tile = [
            self.right,
            self.down,
            self.left,
            self.up,
        ][face]

        # print(self.tile_type, face, step, self.row, self.column)
        if next_tile.tile_type=='#' or step==0:
            return self
        # print(next_tile.row, next_tile.column)
        return next_tile.get_next_tile(face, step-1)

    # get_next_tile(face_handler.face, step)
    
    def add_right_tile(self, right_tile):
        self.right = right_tile
        self.right.left = self
    
    def add_down_tile(self, down_tile):
        self.down = down_tile
        self.down.up = self

    def get_top_most_tile(self):
        next_tile = self
        while True:
            if next_tile.up is None:
                return next_tile
            next_tile = next_tile.up
    
    def print_coor(self):
        print(f'{self.row}_{self.column}')

@dataclass
class FaceHandler:

    def __init__(self, face=0):
        self.face_total = 4
        self.face = 0
    
    def rotate_c(self):
        self.face+=1
        self.face%=self.face_total
        return self.face

    def rotate_cc(self):
        self.face-=1
        if self.face < 0:
            self.face = self.face_total - 1
        return self.face


def iterate_input_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.replace('\n', '')

def main():
    lines = []
    max_col_len = 0
    for line in iterate_input_file_lines(INPUT_FILE):
        lines.append(line)
    
    map_lines = lines[:-2]
    password_line = lines[-1]

    coor_to_key = lambda row, column: f'{row}_{column}'

    # create tile graph
    sim_starting_tile = None
    tile_graph_dict = {}
    current_tile = None
    for i, line in enumerate(map_lines):
        row = i+1
        leftmost_tile = None
        previous_tile = None
        for j, tile_type in enumerate(line):
            max_col_len = max(max_col_len, len(line))
            if tile_type == ' ':
                continue            
            column = j+1
            tile_key = coor_to_key(row, column)
            tile_graph_dict[tile_key] = Tile(row=row, column=column, tile_type=tile_type)
            current_tile = tile_graph_dict[tile_key]

            if sim_starting_tile is None:
                sim_starting_tile = current_tile

            if leftmost_tile is None:
                leftmost_tile = current_tile
                previous_tile = leftmost_tile
                continue
            
            previous_tile.add_right_tile(current_tile)
            previous_tile = current_tile
        
        current_tile.add_right_tile(leftmost_tile)

        if row==1:
            continue

        for k in range(max_col_len):
            col = k+1
            key_a = coor_to_key(row-1, col)
            if key_a not in tile_graph_dict.keys():
                continue
            key_b = coor_to_key(row, col)
            if key_b not in tile_graph_dict.keys():
                top_most_tile = tile_graph_dict[key_a].get_top_most_tile()
                tile_graph_dict[key_a].add_down_tile(top_most_tile)
                continue
            tile_graph_dict[key_a].add_down_tile(tile_graph_dict[key_b])
        
        
    for k in range(max_col_len):
        col = k+1
        key_a = coor_to_key(len(map_lines), col)
        if key_a not in tile_graph_dict.keys():
            continue
        top_most_tile = tile_graph_dict[key_a].get_top_most_tile()
        tile_graph_dict[key_a].add_down_tile(top_most_tile)
        
    # simulate
    
    step_list = []
    buffer = ''
    for item in password_line:
        if item == 'L' or item == 'R':
            step_list.append(buffer)
            buffer = ''
            step_list.append(item)
            continue
        buffer = buffer + item
    if buffer: step_list.append(buffer)

    face_handler = FaceHandler(0)
    current_tile = sim_starting_tile
    for item in step_list:
        # print(current_tile.row, current_tile.column)
        if item.isdigit():
            step = int(item)
            current_tile = current_tile.get_next_tile(face_handler.face, step)
        if item=='L':
            face_handler.rotate_cc()
            continue
        if item=='R':
            face_handler.rotate_c()
            continue
    
    print(current_tile.row)
    print(current_tile.column)
    print(face_handler.face)

    print(1000*current_tile.row + 4*current_tile.column + face_handler.face)

    # tile_graph_dict['200_18'].down.print_coor()
    # # sim_starting_tile.right.print_coor()
        





if __name__=='__main__':
    main()