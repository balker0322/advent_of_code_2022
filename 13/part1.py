from input import input_obj
# from test_input import input_obj
from copy import deepcopy

def is_in_correct_order(left, right):
    left = deepcopy(left)
    right = deepcopy(right)

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 'True'
        if left > right:
            return 'False'
        return 'None'

    if isinstance(left, int) and isinstance(right, list):
        return is_in_correct_order([left], right)

    if isinstance(left, list) and isinstance(right, int):
        return is_in_correct_order(left, [right])

    while True:
        if (not left) and right:
            return 'True'
        if (not right) and left:
            return 'False'
        if (not right) and (not left):
            return 'None'
        result = is_in_correct_order(left[0], right[0])
        if result != 'None':
            return result
        left.remove(left[0])
        right.remove(right[0])


def main():

    total = 0
    for i in range(input_obj.total_item):
        if is_in_correct_order(input_obj.left[i], input_obj.right[i]) == 'True':
            total += (i+1)
    print(total)

if __name__=='__main__':
    main()