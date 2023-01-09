INPUT_FILE = r'input_file.txt'


def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()


def visibility_check(tree_list:list, viewer_height=-1, reverse_tree_list=False):
    score = 0

    if not tree_list:
        return 0

    if reverse_tree_list:
        tree_list = list(tree_list)
        tree_list.reverse()

    for tree in tree_list:
        score += 1
        if tree >= viewer_height:
            return score
    
    return score

def main(input_file=INPUT_FILE):
    tree_table = [[int(x) for x in line] for line in iterate_input_file_lines(input_file)]

    max_score = 0
    for row, tree_row in enumerate(tree_table):
        for col, tree in enumerate(tree_row):
            down = visibility_check([x[col] for x in tree_table[row+1:]], viewer_height=tree, reverse_tree_list=False)
            left = visibility_check([x for x in tree_table[row][:col]], viewer_height=tree, reverse_tree_list=True)
            up = visibility_check([x[col] for x in tree_table[:row]], viewer_height=tree, reverse_tree_list=True)
            right = visibility_check([x for x in tree_table[row][col+1:]], viewer_height=tree, reverse_tree_list=False)
            score = down*left*up*right
            if score > max_score:
                max_score = score
    
    print(max_score)


if __name__=='__main__':
    main()