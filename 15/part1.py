INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def get_manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def get_no_beacon_coor_list(s, b, y_filter=None):
    no_beacon_coor_list = []
    max_distance = get_manhattan_distance(s, b)
    for i in range(-max_distance, max_distance+1):
        dummy = [s[0] + i, y_filter]
        if get_manhattan_distance(s, dummy) <= max_distance:
            no_beacon_coor_list.append(dummy)
    if b in no_beacon_coor_list:
        no_beacon_coor_list.remove(b)
    return no_beacon_coor_list

def main(input_file=INPUT_FILE):
    monitored_y = 2000000
    no_beacon_locations = []
    beacon_locations = []
    coor_to_key = lambda x: f'{x[0]}_{x[1]}'
    for line in iterate_input_file_lines(INPUT_FILE):
        tokens = line.split()
        sx = int(tokens[2].replace(',', '').split('=')[-1])
        sy = int(tokens[3].replace(':', '').split('=')[-1])
        bx = int(tokens[8].replace(',', '').split('=')[-1])
        by = int(tokens[9].split('=')[-1])
        beacon_locations.append([bx, by])
        for coor in get_no_beacon_coor_list([sx, sy], [bx, by], y_filter=monitored_y):
            no_beacon_locations.append(coor_to_key(coor))

    print(len(set(no_beacon_locations)))
    
    

if __name__=='__main__':
    main()