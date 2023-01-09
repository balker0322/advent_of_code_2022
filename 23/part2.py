import time

INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def coor_to_key(x, y):
    return f'{x}_{y}'

class DirectionHanler:

    def __init__(self) -> None:
        self.direction_list = [
            'north',
            'south',
            'west',
            'east',
        ]
        self.adjacent_coor_diff = {
            'north' :[(-1, -1), (-1, 0), (-1, 1)],
            'south' :[(1, -1), (1, 0), (1, 1)],
            'west'  :[(-1, -1), (0, -1), (1, -1)],
            'east'  :[(-1, 1), (0, 1), (1, 1)],
        }
        self.all_adjacent_coor_diff = set([
            (-1, -1), (-1, 0), (-1, 1),
            (1, -1), (1, 0), (1, 1),
            (-1, -1), (0, -1), (1, -1),
            (-1, 1), (0, 1), (1, 1),
        ])
        
    def get_direction_list(self):
        return self.direction_list
    
    def rotate_direction_list(self):
        self.direction_list.append(self.direction_list.pop(0))
    
    def get_side_coor_list(self, direction, elf_coor):
        i, j = elf_coor
        return [(i+a, j+b) for a, b in self.adjacent_coor_diff[direction]]
    
    def get_adjacent_coor(self, direction, elf_coor):
        return self.get_side_coor_list(direction, elf_coor)[1]

    def get_all_adjacent_coor(self, elf_coor):
        i, j = elf_coor
        return [(i+a, j+b) for a, b in self.all_adjacent_coor_diff]

class Elf:

    def __init__(self, row, column):
        self.current_coor = (row, column)
        self.planned_coor = None
    
    def set_planned_coor(self, planned_coor):
        self.planned_coor = planned_coor
    
    def set_planned_to_current_coor(self):
        is_change = self.current_coor != self.planned_coor
        self.current_coor = self.planned_coor
        return is_change
    
    def get_current_coor(self):
        return self.current_coor
    
    def get_planned_coor(self):
        return self.planned_coor

class Simulator:
    
    def __init__(self, direction_handler, elves_list):
        self.direction_handler = direction_handler
        self.elves_list = elves_list
        self.current_elves_coor_list = []
        self.update_current_coor_list()
    
    def rotate_direction_list(self):
        self.direction_handler.rotate_direction_list()
    
    def update_current_coor_list(self):
        self.current_elves_coor_list = set([])
        for elf in self.elves_list:
            self.current_elves_coor_list.add(elf.get_current_coor())
        
    def identify_planned_coor(self):

        for elf in self.elves_list:

            current_coor = elf.get_current_coor()
            elf.set_planned_coor(current_coor)

            if all([x not in self.current_elves_coor_list for x in self.direction_handler.get_all_adjacent_coor(current_coor)]):
                continue

            for direction in self.direction_handler.get_direction_list():

                side_is_free = True
                
                side_coor_list = self.direction_handler.get_side_coor_list(direction, current_coor)

                side_is_free = True
                if any([side_coor in self.current_elves_coor_list for side_coor in side_coor_list]):
                    side_is_free = False

                if side_is_free:
                    planned_coor = self.direction_handler.get_adjacent_coor(direction, current_coor)
                    elf.set_planned_coor(planned_coor)
                    break

    def set_new_coor(self):
        p_coor_dict = {}
        for elf in self.elves_list:
            p_coor = elf.get_planned_coor()
            p_coor_dict[p_coor] = p_coor_dict.get(p_coor, 0) + 1
        
        p_coor_overlap_list = [coor for coor, count in p_coor_dict.items() if count > 1]

        no_changes = True
        changed_count = 0
        for elf in self.elves_list:
            if elf.get_planned_coor() not in p_coor_overlap_list:
                coor_has_changed = elf.set_planned_to_current_coor()
                if coor_has_changed:
                    no_changes = False
                    continue
                changed_count += 1
        # print(f'changed_count: {changed_count}')
        
        self.update_current_coor_list()
        return no_changes
    
    def get_current_coor_range(self):
        row_min, row_max, col_min, col_max = [None for _ in range(4)]
        is_first_loop = True
        for elf in self.elves_list:
            row, col = elf.get_current_coor()
            if is_first_loop:
                row_min, row_max, col_min, col_max = row, row, col, col
                is_first_loop = False
                continue
            row_min, row_max = min(row_min, row), max(row_max, row)
            col_min, col_max = min(col_min, col), max(col_max, col)
        return row_min, row_max, col_min, col_max

    def get_empty_coor_count(self):
        row_min, row_max, col_min, col_max = self.get_current_coor_range()

        empty_coor_count = 0
        for row in range(row_min, row_max+1):
            for col in range(col_min, col_max+1):
                if (row, col) not in self.current_elves_coor_list:
                    empty_coor_count += 1
        
        return empty_coor_count
    
    def print_elves(self):
        row_min, row_max, col_min, col_max = self.get_current_coor_range()

        for row in range(row_min, row_max+1):
            for col in range(col_min, col_max+1):
                sym = '.'
                if (row, col) in self.current_elves_coor_list:
                    sym = '#'
                print(sym, end='')
            print()


def main():

    elves_list = []
    for i, line in enumerate(iterate_input_file_lines(INPUT_FILE)):
        for j, item in enumerate(line):
            if item == '#':
                elves_list.append(Elf(i, j))

    # total_rounds = 10
    direction_handler = DirectionHanler()
    sim = Simulator(direction_handler, elves_list)

    # sim.print_elves()
    # print()

    round = 0
    while True:
        round+=1
        print(f'round {round}')
        sim.identify_planned_coor()
        no_change = sim.set_new_coor()
        if no_change:
            break
        sim.rotate_direction_list()
        
    print(sim.get_empty_coor_count())

if __name__=='__main__':
    main()