INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

class Monkey:

    def __init__(self, name) -> None:
        self.name = name
        self.num = None
        self.m1 = None
        self.m2 = None
        self.operation = None
        self.parent = None
        self.neighbor = None
        self.line = None
        self.is_left = True
    
    def set_line(self, line):
        self.line = line

    def set_job(self, m1, m2, operation):
        self.m1 = m1
        self.m2 = m2
        self.operation = operation

    def set_num(self,num):
        self.num = num
    
    def get_operation(self):
        operation = {
            '+':lambda x, y: x+y,
            '-':lambda x, y: x-y,
            '*':lambda x, y: x*y,
            '/':lambda x, y: x/y,
        }
        return operation[self.operation]
    
    def get_inv_operation(self):
        operation = {
            '+':lambda x, y: x-y,
            '-':lambda x, y: x+y,
            '*':lambda x, y: x/y,
            '/':lambda x, y: x*y,
        }
        return operation[self.operation]
    
    def get_num(self):
        if self.num is not None:
            return self.num
        if self.operation == None:
            return None
        num1 = self.m1.get_num()
        num2 = self.m2.get_num()
        if num1 is None or num2 is None:
            return None
        self.num = self.get_operation()(num1, num2)
        return self.num

    def get_expected_value(self):
        if self.num is not None:
            return self.num

        operation = self.parent.get_inv_operation()
        result_num = self.parent.get_expected_value()
        neighbor_num = self.neighbor.get_num()

        if self.parent.operation in ['+', '*'] or self.is_left:
            operation = self.parent.get_inv_operation()
            self.num = operation(result_num, neighbor_num)
        else:        
            operation = self.parent.get_operation()
            self.num = operation(neighbor_num, result_num)

        return self.get_num()

def parse_input():
    monkeys = {}
    for line in iterate_input_file_lines(INPUT_FILE):
        name, job = line.split(': ')
        monkeys[name] = monkeys.get(name, Monkey(name))
        current_monkey = monkeys[name]
        current_monkey.set_line(line)
        if name =='humn':
            continue
        if job.isnumeric():
           current_monkey.set_num(float(job))
           continue 
        m1, operation, m2 = job.split()
        monkeys[m1] = monkeys.get(m1, Monkey(m1))
        monkeys[m1].is_left = True
        monkeys[m2] = monkeys.get(m2, Monkey(m2))
        monkeys[m2].is_left = False
        if name == 'root':
            tree1, _, tree2 = job.split()
            operation = '='
            current_monkey.set_job(monkeys[m1], monkeys[m2], operation)
            continue

        monkeys[m1].parent = current_monkey
        monkeys[m1].neighbor = monkeys[m2]
        monkeys[m2].parent = current_monkey
        monkeys[m2].neighbor = monkeys[m1]
        
        current_monkey.set_job(monkeys[m1], monkeys[m2], operation)
    
    return monkeys, tree1, tree2

def main():
    monkeys, tree1, tree2 = parse_input()
    
    ans = monkeys[tree1].get_num()
    if ans is None:
        ans = monkeys[tree2].get_num()
    monkeys[tree1].set_num(ans)
    monkeys[tree2].set_num(ans)
    print(ans)
    x = monkeys['humn'].get_expected_value()
    monkeys, tree1, tree2 = parse_input()

    monkeys['humn'].set_num(x)
    print('humn', monkeys['humn'].get_num())
    print(tree1, monkeys[tree1].get_num())
    print(tree2, monkeys[tree2].get_num())
    

if __name__=='__main__':
    main()