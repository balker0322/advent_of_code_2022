INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def get_list_expansion(p1, p2):
    def get_list(a, b):
        delta = 1
        if a > b:
            delta = -1
        return [x for x in range(a, b+delta, delta)]
    if p1[0] == p2[0]:
        return [[p1[0], x] for x in get_list(p1[1], p2[1])]
    return [[x, p1[1]] for x in get_list(p1[0], p2[0])]

def main():
    coor_to_key = lambda x: f'{x[0]}_{x[1]}'
    grid_mark_dict = {}
    max_depth = 0
    for line in iterate_input_file_lines(INPUT_FILE):
        rock_corners = [[int(x) for x in coor.split(',')] for coor in line.split(' -> ')]
        for i in range(len(rock_corners[:-1])):
            for rock_coor in get_list_expansion(rock_corners[i], rock_corners[i+1]):
                grid_mark_dict[coor_to_key(rock_coor)] = 1
                if rock_coor[1] > max_depth:
                    max_depth = rock_coor[1]
    starting_coor = [500, 0]

    stop_sim = False

    while not stop_sim:

        current_coor = list(starting_coor)
        
        while True:
            ci, cj = current_coor

            if cj+1 > max_depth:
                stop_sim = True
                break
            
            is_at_rest = True
            for i in [0, -1, 1]:
                ni, nj = ci+i, cj+1                
                if grid_mark_dict.get(coor_to_key([ni, nj]), 0) == 0:
                    current_coor = [ni, nj]
                    is_at_rest = False
                    break

            if not is_at_rest:
                continue
        
            grid_mark_dict[coor_to_key([ci, cj])] = 2
            break

    total = sum([1 for x in grid_mark_dict.values() if x == 2])
    print(total)

if __name__=='__main__':
    main()