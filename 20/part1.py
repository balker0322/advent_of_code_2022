INPUT_FILE = r'input_file.txt'

class Node:

    def __init__(self, data):
        self.data = data
        self.previous = None
        self.next = None
    
    def set_next_node(self, next_node):
        self.next = next_node
        self.next.previous = self

def swap_node(node_a:Node, node_b:Node):
    # assuming two nodes are adjacent
    node1, node2, node3, node4 = node_a.previous, node_a, node_b, node_b.next
    if node_b.next == node_a:
        # print('not')
        node1, node2, node3, node4 = node_b.previous, node_b, node_a, node_a.next
    node1.set_next_node(node3)
    node3.set_next_node(node2)
    node2.set_next_node(node4)

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def main():
    node_list = []
    previous_node = None
    zero_node = None
    n = None
    for line in iterate_input_file_lines(INPUT_FILE):
        data = int(line)
        n = Node(data)
        if data==0:
            zero_node=n
        node_list.append(n)
        if previous_node is not None:
            previous_node.set_next_node(n)        
        previous_node = n
    n.set_next_node(node_list[0])

    def print_node_list():
        l = []
        curr_node = zero_node
        while True:
            l.append(curr_node.data)
            if len(l) > len(node_list)-1:
                break
            curr_node = curr_node.next
        print(l)
        
    for node in node_list:
        for _ in range(abs(node.data)):
            other_node = node.next
            if node.data < 0:
                other_node = node.previous
            swap_node(node, other_node)

    i = 1
    total = 0
    current_node = zero_node
    while True:
        current_node = current_node.next
        if i==1000:
            total+=current_node.data
            print(1000, current_node.data)
        if i==2000:
            total+=current_node.data
            print(2000, current_node.data)
        if i==3000:
            total+=current_node.data
            print(3000, current_node.data)
            break
        i+=1
    print(total)

if __name__=='__main__':
    main()