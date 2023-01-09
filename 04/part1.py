INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')

def main():
    total_overalap = 0
    for line in iterate_input_file_lines(INPUT_FILE):
        [p1a, p1b], [p2a, p2b] = [[int(y) for y in x.split('-')] for x in line.split(',')]
        if max(p1b, p2b) - min(p1a, p2a) <= max(p1b - p1a, p2b - p2a):
            total_overalap += 1
    print(total_overalap)
    
if __name__=='__main__':
    main()