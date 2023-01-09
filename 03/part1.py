INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')

def split_per_compartment(line:str):
    split_len = int(len(line)/2)
    return [line[:split_len], line[split_len:]]

def get_common_item_in_list(item_list):
    for item in item_list[0]:
        if item in item_list[1]:
            return item

def get_priority(item):
    item_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return item_list.index(item)+1


def main():
    total_priority = sum([get_priority(get_common_item_in_list(split_per_compartment(line))) for line in iterate_input_file_lines(INPUT_FILE)])
    print(total_priority)

if __name__=='__main__':
    main()