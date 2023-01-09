INPUT_FILE = r'input_file.txt'

class Monkey:

    def __init__(self, item_list, update_value_func, digit_multiple):
        self.item_list = item_list
        self.update_value_func = update_value_func
        self.digit_multiple = digit_multiple
        self.inspect_count = 0

    def set_throw_target(self, monkey_a, monkey_b):
        self.monkey_a = monkey_a
        self.monkey_b = monkey_b
    
    def take_turn(self):
        while self.item_list:
            self.inspect_count += 1
            item = int(self.update_value_func(self.item_list.pop())/3)
            if item%self.digit_multiple==0:
                self.monkey_a.item_list.append(item)
                continue
            self.monkey_b.item_list.append(item)

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def main():
    round = 20
    m = [
        Monkey([56, 56, 92, 65, 71, 61, 79], lambda x: x*7, 3),
        Monkey([61, 85], lambda x: x+5, 11),
        Monkey([54, 96, 82, 78, 69], lambda x: x*x, 7),
        Monkey([57, 59, 65, 95], lambda x: x+4, 2),
        Monkey([62, 67, 80], lambda x: x*17, 19),
        Monkey([91], lambda x: x+7, 5),
        Monkey([79, 83, 64, 52, 77, 56, 63, 92], lambda x: x+6, 17),
        Monkey([50, 97, 76, 96, 80, 56], lambda x: x+3, 13),
    ]
    m[0].set_throw_target(m[3], m[7])
    m[1].set_throw_target(m[6], m[4])
    m[2].set_throw_target(m[0], m[7])
    m[3].set_throw_target(m[5], m[1])
    m[4].set_throw_target(m[2], m[6])
    m[5].set_throw_target(m[1], m[4])
    m[6].set_throw_target(m[2], m[0])
    m[7].set_throw_target(m[3], m[5])

    for i in range(round):
        for monkey in m:
            monkey.take_turn()
    
    inspect_count_list = [x.inspect_count for x in m]
    inspect_count_list.sort()
    print(inspect_count_list[-2]*inspect_count_list[-1])

if __name__=='__main__':
    main()