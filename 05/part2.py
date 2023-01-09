INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')
            

def main(input_file=INPUT_FILE):
    
    crates_data = [
        list('DHNQTWVB'),
        list('DWB'),
        list('TSQWJC'),
        list('FJRNZTP'),
        list('GPVJMST'),
        list('BWFTN'),
        list('BLDQFHVN'),
        list('HPFR'),
        list('ZSMBLNPH'),
    ]

    for line in iterate_input_file_lines(input_file):
        if not line.startswith('move'):
            continue
        crate_count, source_stack, destination_stack = [int(line.split()[i]) for i in [1, 3, 5]]
        temp_list = []
        for _ in range(crate_count):
            temp_list.append(crates_data[source_stack-1].pop())
        for _ in range(crate_count):
            crates_data[destination_stack-1].append(temp_list.pop())
    
    print(''.join([stack[-1] for stack in crates_data]))


if __name__=='__main__':
    main()