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
    divide_packets = [[[2]], [[6]]]

    packet_list = list(divide_packets)
    for i in range(input_obj.total_item):
        packet_list.append(list(input_obj.left[i]))
        packet_list.append(list(input_obj.right[i]))

    correct_order = False
    while not correct_order:
        correct_order = True
        for i in range(len(packet_list[:-1])):
            if is_in_correct_order(list(packet_list[i]), list(packet_list[i+1]))=='False':
                packet_list[i], packet_list[i+1] = packet_list[i+1], packet_list[i]
                correct_order = False
    
    distress_signal = 1
    for i, p in enumerate(packet_list):
        if p in divide_packets:
            distress_signal *= (i+1)
        
    print(distress_signal)

if __name__=='__main__':
    main()