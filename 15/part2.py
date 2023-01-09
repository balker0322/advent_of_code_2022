INPUT_FILE = r'input_file.txt'

class Point:

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y


class Segment:

    def __init__(self, point1:Point, point2:Point):
        self.point1 = point1
        self.point2 = point2

class Diamond:

    def __init__(self, center:Point, half_diagonal:int):
        self.center = half_diagonal
        self.center = half_diagonal


def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def get_manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def get_no_beacon_coor_list(s, b, max_sx, max_sy, existing_list):
    no_beacon_coor_list = []
    max_distance = get_manhattan_distance(s, b)
    for x_delta in range(-max_distance, max_distance+1):
        x = s[0] + x_delta
        if x > max_sx:
            continue
        max_y_delta = max_distance - abs(x_delta)
        for y_delta in range(-max_y_delta, max_y_delta+1):
            y = s[1] + y_delta
            if y > max_sy:
                continue
            dummy = [x, y]
            if dummy in existing_list:
                continue
            if not b == dummy:
                no_beacon_coor_list.append(dummy)
    return no_beacon_coor_list

def get_set_of_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    delta = 1 if x1 < x2 else -1
    m = (y2-y1)/(x2-x1)
    def calc_y(x):
        return int((x-x1)*m+y1)
    return [[x, calc_y(x)] for x in range(x1, x2+delta,delta)]

def get_corners(pc, d, max_sx, max_sy):
    cx, cy = pc
    return [
        [cx + d, cy],
        [cx, cy + d],
        [cx - d, cy],
        [cx, cy - d],
    ]

def get_no_coverage_coor_list(s, b, max_sx, max_sy):
    no_coverage_coor_list = []
    max_distance = get_manhattan_distance(s, b) + 1
    c1, c2, c3, c4 = get_corners(s, max_distance, max_sx, max_sy)
    no_coverage_coor_list += get_set_of_points(c1, c2)
    no_coverage_coor_list += get_set_of_points(c2, c3)
    no_coverage_coor_list += get_set_of_points(c3, c4)
    no_coverage_coor_list += get_set_of_points(c4, c1)
    return no_coverage_coor_list

def main():
    coor_to_key = lambda x: f'{x[0]}_{x[1]}'
    max_sx = 0
    max_sy = 0
    min_sx = 0
    min_sy = 0
    firstloop = True
    parsed_data = []
    for line in iterate_input_file_lines(INPUT_FILE):
        tokens = line.split()
        sx = int(tokens[2].replace(',', '').split('=')[-1])
        sy = int(tokens[3].replace(':', '').split('=')[-1])
        bx = int(tokens[8].replace(',', '').split('=')[-1])
        by = int(tokens[9].split('=')[-1])
        if firstloop:
            max_sx = sx
            max_sy = sy
            min_sx = sx
            min_sy = sy
            firstloop = False
        min_sx = min(sx, min_sx)
        min_sy = min(sy, min_sy)
        max_sx = max(sx, max_sx)
        max_sy = max(sy, max_sy)
        s = [sx, sy]
        b = [bx, by]
        parsed_data.append([s, b, get_manhattan_distance(s, b)])
    
        def is_in_max_area(p):
            x, y = p
            if x > max_sx:
                return False
            if y > max_sy:
                return False
            if x < min_sx:
                return False
            if y < min_sy:
                return False
            return True
        
        def is_not_in_coverage(p):
            if not is_in_max_area(p):
                return False
            for s, _, d in parsed_data:
                if get_manhattan_distance(s, p) <= d:
                    return False
            return True

    no_coverage_list = []
    i = 0
    for s, b, _ in parsed_data:
        i+=1
        print(i, s, b)
        r = get_no_coverage_coor_list(s, b, max_sx, max_sy)
        no_coverage_list += [p for p in r if is_not_in_coverage(p)]

    x, y = no_coverage_list[0]
    print(4000000*x+y)
    


if __name__=='__main__':
    main()
    # 3303271, 2906101