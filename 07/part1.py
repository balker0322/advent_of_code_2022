INPUT_FILE = r'input_file.txt'


def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')


def main(input_file=INPUT_FILE):

    limit_size = 100000

    dir_dict = {}
    cd_list = []

    for line in iterate_input_file_lines(input_file):

        if line=='$ cd ..':
            cd_list.pop()
            continue
        if line.startswith('$ cd'):
            cd_list.append(line.split()[-1])
            continue
        if not line.startswith('$') and not line.startswith('dir'):
            temp_cd_list = list(cd_list)
            while temp_cd_list:
                cd_key = '-'.join(temp_cd_list)
                if not cd_key in dir_dict.keys():
                    dir_dict[cd_key] = 0
                dir_dict[cd_key] += int(line.split()[0])
                temp_cd_list.pop()
    
    print(sum([size for size in dir_dict.values() if size <= limit_size]))


if __name__=='__main__':
    main()