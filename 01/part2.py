INPUT_FILE = r'input_file.txt'

def get_parsed_input(input_file):
    calories_list = [[]]
    with open(input_file, 'r') as file:
        for line in file.readlines():
            if line.strip():
                calories_list[-1].append(int(line.strip()))
                continue
            calories_list.append([])
    return calories_list

def main():
    calories_total_list = [sum(x) for x in get_parsed_input(INPUT_FILE)]
    calories_total_list.sort(reverse=True)
    print(sum(calories_total_list[:3]))

if __name__=='__main__':
    main()