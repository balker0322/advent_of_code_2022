from dataclasses import dataclass

INPUT_FILE = r'input_file.txt'
tile_graph_dict = {}

@dataclass
class Tile:
    row:int
    column:int
    tile_type:str
    left = None
    right = None
    up = None
    down = None
    applied_rotation = None

    def get_next_tile(self, face_handler, step, applied_rotation=None):

        if applied_rotation is not None:
            self.apply_rotation(face_handler, applied_rotation)

        face_string = face_handler.get_face_string()
        next_tile = self.get_neighbor(face_string)

        self.print_symbol(face_handler)

        if next_tile.tile_type=='#':
            return self

        if step==0:
            return self

        next_applied_rotation = self.get_applied_rotation_value(face_string)
        
        return next_tile.get_next_tile(face_handler, step-1, next_applied_rotation)

    
    def add_right_tile(self, right_tile):
        self.attach_tile(right_tile, 'right', 'left')
    
    def add_down_tile(self, down_tile):
        self.attach_tile(down_tile, 'down', 'up')
    
    def set_right_tile(self, tile):
        self.right = tile
    
    def set_left_tile(self, tile):
        self.left = tile
    
    def set_up_tile(self, tile):
        self.up = tile
    
    def set_down_tile(self, tile):
        self.down = tile

    def get_top_most_tile(self):
        next_tile = self
        while True:
            if next_tile.up is None:
                return next_tile
            next_tile = next_tile.up

    def get_neighbor(self, side):
        return {
            'right':self.right,
            'down':self.down,
            'left':self.left,
            'up':self.up,
        }[side]
    
    def attach_tile(self, tile, from_side, to_side):
        attach_tile = {
            'right': lambda f,t: f.set_right_tile(t),
            'down':  lambda f,t: f.set_down_tile(t),
            'left':  lambda f,t: f.set_left_tile(t),
            'up':    lambda f,t: f.set_up_tile(t),
        }
        rotation_index = {
            'right': (0,2),
            'down':  (1,3),
            'left':  (2,0),
            'up':    (3,1),
        }
        attach_tile[from_side](self, tile)
        attach_tile[to_side](tile, self)
        # rotation_index[to_side][1] - rotation_index[from_side][0]
        self.set_applied_rotation_value(from_side, rotation_index[to_side][1] - rotation_index[from_side][0])
        tile.set_applied_rotation_value(to_side, rotation_index[from_side][0] - rotation_index[to_side][1])
        # self.applied_rotation[from_side] = rotation_index[to_side][1] - rotation_index[from_side][0]
        if f'{self.row}_{self.column}_{from_side}' == '1_11_down':
            print(f'{self.row}_{self.column}_{from_side} {self.applied_rotation[from_side]}')
    
    def set_applied_rotation_value(self, side, value):
        if self.applied_rotation is None:
            self.applied_rotation = {}
        self.applied_rotation[side] = value
    
    def get_applied_rotation_value(self, side):
        return self.applied_rotation.get(side, 0)

    def apply_rotation(self, face_handler, applied_rotation):
        rotation_func = face_handler.rotate_c
        if applied_rotation < 0:
            rotation_func = face_handler.rotate_cc
        rotate = abs(int(applied_rotation))
        while rotate:
            rotation_func()
            rotate-=1

    def print_coor(self):
        print(f'{self.row}_{self.column}')

    def print_symbol(self, face_handler):
        print(f'{self.row}_{self.column} {face_handler.get_face_symbol()}')


@dataclass
class BigTile:
    upper_left = None
    upper_right = None
    lower_left = None
    lower_right = None
    side_len:int = 0

    def add_row(self, row):
        self.side_len = len(row)

        if self.lower_left is not None:
            upper_item = self.lower_left
            for item in row:
                upper_item.attach_tile(item, 'down', 'up')
                upper_item = upper_item.right
                # print('==', end='')
                # item.print_coor()
                # upper_item = upper_item.get_neighbor('right')


        previous_item = None
        for item in row:
            if self.upper_left is None:
                self.upper_left = item
            
            if previous_item is None:
                previous_item = item
                continue

            previous_item.attach_tile(item, 'right', 'left')
            previous_item = item
        
        if self.upper_right is None:
            self.upper_right = row[-1]
        
        self.lower_left, self.lower_right = row[0], row[-1]
    

    def print_big_tile(self):
        current_tile = self.upper_left
        for _ in range(self.side_len):
            self.print_row(current_tile)
            print()
            current_tile = current_tile.down
        
    def print_row(self, tile):
        current_tile = tile
        for _ in range(self.side_len):
            # current_tile.print_coor()
            tile_type = current_tile.tile_type
            # print(tile_type, end='')
            row = current_tile.row
            col = current_tile.column
            print(f'{row}_{col}', end=' | ')
            current_tile = current_tile.right

    def attach_big_tile(self, side, other_big_tile, other_side):
        
    # big_tile_dict['2_1'].attach_big_tile('down', big_tile_dict['3_3'], 'down')

        data = {
            'right' : [ self.upper_right, other_big_tile.lower_right, 'down',  'up',    ],
            'down'  : [ self.lower_right, other_big_tile.lower_left,  'left',  'right', ],
            'left'  : [ self.lower_left,  other_big_tile.upper_left,  'up',    'down',  ],
            'up'    : [ self.upper_left,  other_big_tile.upper_right, 'right', 'left',  ],
        }

        this_tile = data[side][0]
        other_tile = data[other_side][1]

        for _ in range(self.side_len):
            this_tile.attach_tile(other_tile, side, other_side)
            this_tile = this_tile.get_neighbor(data[side][2])
            other_tile = other_tile.get_neighbor(data[other_side][3])


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
    
    def get_face_string(self):
        return [
            'right',
            'down',
            'left',
            'up',
        ][self.face]
    
    def get_face_symbol(self):
        return [
            '>',
            'V',
            '<',
            '^',
        ][self.face]


def iterate_input_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.replace('\n', '')

def main():
    coor_to_key = lambda row, column: f'{row}_{column}'
    lines = []
    max_col_len = 0
    for line in iterate_input_file_lines(INPUT_FILE):
        lines.append(line)
    
    map_lines = lines[:-2]
    password_line = lines[-1]
    cube_side_len = sorted(set([len(x) for x in map_lines]))
    cube_side_len = cube_side_len[-1] - cube_side_len[-2]
    print(f'cube_side_len: {cube_side_len}')

    row = 0
    big_tile_dict = {}
    # tile_graph_dict = {}
    while row < len(map_lines):
        for i, line in enumerate(map_lines[row:row+cube_side_len]):
            # print()
            row_i = row + i + 1
            column = 0
            while column < len(line):
                item_list = []
                # print()
                # print(f'row:{row}, column:{column}')
                for j, item in enumerate(line[column:column+cube_side_len]):
                    column_j = column + j + 1
                    # print(row_i, column_j, item, end=' - ')
                    # tile_item = Tile(row=row_i, column=column_j, tile_type=item)
                    tile_key=coor_to_key(row_i, column_j)
                    # tile_graph_dict[tile_key] = tile_item
                    # item_list.append(tile_item)
                    tile_graph_dict[tile_key] = tile_graph_dict.get(tile_key, Tile(row=row_i, column=column_j, tile_type=item))
                    item_list.append(tile_graph_dict[tile_key])
                big_tile_key = coor_to_key(int(row/cube_side_len)+1, int(column/cube_side_len)+1)
                big_tile_dict[big_tile_key] = big_tile_dict.get(big_tile_key, BigTile(cube_side_len))
                big_tile_dict[big_tile_key].add_row(item_list)
                column+=cube_side_len
        row+=cube_side_len

    
    # for key, value in big_tile_dict.items():
    #     print()
    #     print(key)
    #     value.print_big_tile()


    # test

    # big_tile_dict['2_3'].attach_big_tile('up', big_tile_dict['1_3'], 'down')
    # big_tile_dict['2_3'].attach_big_tile('down', big_tile_dict['3_3'], 'up')
    # big_tile_dict['2_3'].attach_big_tile('left', big_tile_dict['2_2'], 'right')
    # big_tile_dict['2_3'].attach_big_tile('right', big_tile_dict['3_4'], 'up')
    # big_tile_dict['2_1'].attach_big_tile('up', big_tile_dict['1_3'], 'up')
    # big_tile_dict['2_1'].attach_big_tile('down', big_tile_dict['3_3'], 'down')
    # big_tile_dict['2_1'].attach_big_tile('left', big_tile_dict['3_4'], 'down')
    # big_tile_dict['2_1'].attach_big_tile('right', big_tile_dict['2_2'], 'left')
    # big_tile_dict['2_2'].attach_big_tile('up', big_tile_dict['1_3'], 'left')
    # big_tile_dict['1_3'].attach_big_tile('left', big_tile_dict['3_4'], 'left')
    # big_tile_dict['3_4'].attach_big_tile('left', big_tile_dict['3_3'], 'right')
    # big_tile_dict['3_3'].attach_big_tile('left', big_tile_dict['2_2'], 'down')
    # sim_starting_tile = big_tile_dict['1_3'].upper_left

    
    big_tile_dict['3_2'].attach_big_tile('up', big_tile_dict['2_2'], 'down')
    big_tile_dict['3_2'].attach_big_tile('down', big_tile_dict['4_1'], 'right')
    big_tile_dict['3_2'].attach_big_tile('left', big_tile_dict['3_1'], 'right')
    big_tile_dict['3_2'].attach_big_tile('right', big_tile_dict['1_3'], 'right')

    big_tile_dict['1_2'].attach_big_tile('up', big_tile_dict['4_1'], 'left')
    big_tile_dict['1_2'].attach_big_tile('down', big_tile_dict['2_2'], 'up')
    big_tile_dict['1_2'].attach_big_tile('left', big_tile_dict['3_1'], 'left')
    big_tile_dict['1_2'].attach_big_tile('right', big_tile_dict['1_3'], 'left')

    big_tile_dict['3_1'].attach_big_tile('down', big_tile_dict['4_1'], 'up')
    big_tile_dict['2_2'].attach_big_tile('left', big_tile_dict['3_1'], 'up')
    big_tile_dict['1_3'].attach_big_tile('down', big_tile_dict['2_2'], 'right')
    big_tile_dict['4_1'].attach_big_tile('down', big_tile_dict['1_3'], 'up')

    sim_starting_tile = big_tile_dict['1_2'].upper_left

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
            current_tile = current_tile.get_next_tile(face_handler, step)
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