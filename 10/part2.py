INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()
    
def get_new_pixel(cycle_counter, register_x):
    if cycle_counter-1 in [register_x-1, register_x, register_x+1]:
        return '#'
    return '.'

def update_crt_value(crt_list, cycle_counter, register_x):
    new_crt_values = list(crt_list)
    new_crt_values[-1].append(get_new_pixel(cycle_counter%40, register_x))
    if len(new_crt_values[-1])==40:
        new_crt_values.append([])
    return new_crt_values

def main():
    cycle_counter = 0
    register_x = 1
    crt_list = [[]]
    for line in iterate_input_file_lines(INPUT_FILE):
        cycle_counter += 1
        crt_list = update_crt_value(crt_list, cycle_counter, register_x)
        if line.split()[0] == 'addx':
            cycle_counter += 1
            crt_list = update_crt_value(crt_list, cycle_counter, register_x)
            register_x += int(line.split()[-1])
    
    for row in crt_list:
        for pixel in row:
            print(pixel, end='')
        print()

if __name__=='__main__':
    main()