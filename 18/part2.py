INPUT_FILE = r'input.txt'

def iterate_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as f:
        for line in f:
            yield line.strip()

def main():
    total_area = 0
    areas_count = {}
    for line in iterate_file_lines():
        x, y, z = [int(num) for num in line.split(',')]
        areas_count[f'{"x"}_{y}_{z}'] = areas_count.get(f'{"x"}_{y}_{z}', []) + [x]
        areas_count[f'{x}_{"y"}_{z}'] = areas_count.get(f'{x}_{"y"}_{z}', []) + [y]
        areas_count[f'{x}_{y}_{"z"}'] = areas_count.get(f'{x}_{y}_{"z"}', []) + [z]
        total_area += 6
    
    overlaps_area = 0
    for key, pos in areas_count.items():
        # if len(pos)%2==0:
        #     overlaps_area += 1
        sorted_pos = sorted(list(pos), reverse=True)
        print(key, sorted_pos)
        # for i in range(len(sorted_pos)-1):
        #     if sorted_pos[i] - sorted_pos[i+1] == 1:
        #         overlaps_area += 2
        x, _ = divmod(len(sorted_pos), 2)
        for i in range(x):
            overlaps_area += 2
        


    # overlaps_area = sum([1 for a in areas_count.values() if a > 1])
    print(total_area)
    total_area -= overlaps_area

    # total_area = sum([2 for _ in areas_count])

    print(total_area)

def get_total_surface_area(coor_key_list):
    total_area = 0
    areas_count = {}
    for line in coor_key_list:
        x, y, z = [int(num) for num in line.split('_')]
        areas_count[f'{"x"}_{y}_{z}'] = areas_count.get(f'{"x"}_{y}_{z}', []) + [x]
        areas_count[f'{x}_{"y"}_{z}'] = areas_count.get(f'{x}_{"y"}_{z}', []) + [y]
        areas_count[f'{x}_{y}_{"z"}'] = areas_count.get(f'{x}_{y}_{"z"}', []) + [z]
        total_area += 6
    
    overlaps_area = 0
    for pos in areas_count.values():
        sorted_pos = sorted(list(pos), reverse=True)
        for i in range(len(sorted_pos)-1):
            if sorted_pos[i] - sorted_pos[i+1] == 1:
                overlaps_area += 2
    
    return total_area - overlaps_area
        

def coor_to_key(x, y, z):
    func = lambda x,y,z: f'{x}_{y}_{z}'
    return func(x, y, z)


def get_neighbors(key, limits):
    x, y, z = [int(x) for x in key.split('_')]
    neighbors = [
        [x+1, y, z], [x-1, y, z],
        [x, y+1, z], [x, y-1, z],
        [x, y, z+1], [x, y, z-1],
    ]
    return [coor_to_key(a,b,c) for a,b,c in neighbors if not out_of_bounds(coor_to_key(a,b,c), limits)]

def out_of_bounds(key, limits):
    x_min, x_max, y_min, y_max, z_min, z_max = limits
    x, y, z = [int(x) for x in key.split('_')]
    if x < x_min or x > x_max or y < y_min or y > y_max or z < z_min or z > z_max:
        return True
    return False

def main2():
    
    lava = set([])
    external = set([])
    internal = set([])
    first_scan = True
    for line in iterate_file_lines():
        x, y, z = [int(num) for num in line.split(',')]
        lava.add(coor_to_key(x, y, z))
        if first_scan:
            x_min, x_max = x, x
            y_min, y_max = y, y
            z_min, z_max = z, z
            first_scan = False
        x_min, x_max = min(x_min, x-2), max(x_max, x+2)
        y_min, y_max = min(y_min, y-2), max(y_max, y+2)
        z_min, z_max = min(z_min, z-2), max(z_max, z+2)
    limits = [x_min, x_max, y_min, y_max, z_min, z_max]


    # fill external
    front = coor_to_key(x_min, y_min, z_min)
    external.add(front)
    queue = [front]
    visited = set([])

    while queue:
        front = queue[0]
        for neighbor in [x for x in get_neighbors(front, limits) if (not x in visited) and (not x in lava)]:
            if neighbor not in queue: queue.append(neighbor)
            external.add(neighbor)
        visited.add(queue.pop(0))
    
    # get all internal
    front = coor_to_key(x_min, y_min, z_min)
    external.add(front)
    queue = [front]
    visited = set([])

    while queue:
        front = queue[0]
        for neighbor in [x for x in get_neighbors(front, limits) if (not x in visited)]:
            if neighbor not in queue: queue.append(neighbor)
            if neighbor in lava:
                continue
            if neighbor in external:
                continue
            internal.add(neighbor)
        visited.add(queue.pop(0))

    print(get_total_surface_area(lava) - get_total_surface_area(internal))


if __name__=='__main__':
    main2()