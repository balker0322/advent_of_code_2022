INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')

def main():
    window_len = 4

    line = [x for x in iterate_input_file_lines(INPUT_FILE)][0]
    
    i = 0
    while True:
        if len(set(line[i:i+window_len]))==window_len:
            print(i+window_len)
            break
        i += 1

if __name__=='__main__':
    main()