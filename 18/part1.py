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
        sorted_pos = sorted(list(pos), reverse=True)
        print(key, sorted_pos)
        for i in range(len(sorted_pos)-1):
            if sorted_pos[i] - sorted_pos[i+1] == 1:
                overlaps_area += 2


    # overlaps_area = sum([1 for a in areas_count.values() if a > 1])
    print(total_area)
    total_area -= overlaps_area

    print(total_area)

if __name__=='__main__':
    main()