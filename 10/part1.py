INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def get_if_in_interest(cycle, reg):
    interest_cycle = [20, 60, 100, 140, 180, 220]
    if cycle in interest_cycle:
        return reg*cycle
    return 0
    
def main():
    cycle_counter = 0
    register_x = 1
    total_sum = 0
    for line in iterate_input_file_lines(INPUT_FILE):
        cycle_counter += 1
        total_sum += get_if_in_interest(cycle_counter, register_x)
        if line.split()[0] == 'addx':  
            cycle_counter += 1
            total_sum += get_if_in_interest(cycle_counter, register_x)
            register_x += int(line.split()[-1])
    print(total_sum)

if __name__=='__main__':
    main()