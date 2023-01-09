INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

class Monkey:

    def __init__(self) -> None:
        self.num = None
        self.m1 = None
        self.m2 = None
        self.expected_num_holder = None
        self.operation = None
    
    def set_expected_num_holder(self, expected_num_holder):
        self.expected_num_holder = expected_num_holder

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
    
    def get_num(self):
        if self.num is not None:
            return self.num
        return self.get_operation()(self.m1.get_num(), self.m2.get_num())
    
def main():
    monkeys = {}
    for line in iterate_input_file_lines(INPUT_FILE):
        name, job = line.split(': ')
        monkeys[name] = monkeys.get(name, Monkey())
        current_monkey = monkeys[name]
        if job.isnumeric():
           current_monkey.set_num(float(job))
           continue 
        m1, operation, m2 = job.split()
        monkeys[m1] = monkeys.get(m1, Monkey())
        monkeys[m2] = monkeys.get(m2, Monkey())
        current_monkey.set_job(monkeys[m1], monkeys[m2], operation)
    
    print(monkeys['root'].get_num())

if __name__=='__main__':
    main()