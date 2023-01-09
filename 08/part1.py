INPUT_FILE = r'input_file.txt'


def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()


def visibility_check(tree_list:list, viewer_height=-1, reverse_tree_list=False):
    tree_visibility_list = []
    if reverse_tree_list:
        tree_list = list(tree_list)
        tree_list.reverse()
    max_tree = viewer_height
    for tree in tree_list:
        if tree > max_tree:
            max_tree = tree
            tree_visibility_list.append(True)
            continue
        tree_visibility_list.append(False)
    if reverse_tree_list:
        tree_visibility_list = list(tree_visibility_list)
        tree_visibility_list.reverse()
    return tree_visibility_list


def main(input_file=INPUT_FILE):
    tree_table = [[int(x) for x in line] for line in iterate_input_file_lines(input_file)]
    tree_visibility_table = [[False for _ in tree] for tree in tree_table]

    for row in range(len(tree_table)):
        a = visibility_check(tree_table[row], reverse_tree_list=False)
        b = visibility_check(tree_table[row], reverse_tree_list=True)
        tree_visibility_table[row] = [any([tree_visibility_table[row][i],a[i],b[i]]) for i in range(len(tree_visibility_table[row]))]

    for col in range(len(tree_table[0])):
        tree_col = [tree_row[col] for tree_row in tree_table]
        a = visibility_check(tree_col, reverse_tree_list=False)
        b = visibility_check(tree_col, reverse_tree_list=True)
        for i in range(len(tree_table)):
            tree_visibility_table[i][col] = any([tree_visibility_table[i][col], a[i], b[i]])
    
    print(sum([sum([1 for item in row if item]) for row in tree_visibility_table]))


if __name__=='__main__':
    main()