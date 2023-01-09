INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()


class RopeNode:

    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y
        self.movements = {
            'DL' : lambda: [self.x - 1, self.y - 1],
            'RD' : lambda: [self.x + 1, self.y - 1],
            'RU' : lambda: [self.x + 1, self.y + 1],
            'LU' : lambda: [self.x - 1, self.y + 1],
            'D' : lambda: [self.x, self.y - 1],
            'L' : lambda: [self.x - 1, self.y],
            'U' : lambda: [self.x, self.y + 1],
            'R' : lambda: [self.x + 1, self.y],
        }
    
    def move(self, direction):
        self.x, self.y = self.movements[direction]()
    
    def is_adjacent(self, another_node):
        if abs(self.x - another_node.x) <= 1 and abs(self.y - another_node.y) <= 1:
            return True
        return False

    def get_distance_score(self, another_node):
        return abs(another_node.x - self.x) + abs(another_node.y - self.y)
    
    def follow(self, another_node):

        if self.is_adjacent(another_node):
            return

        min_score = []
        for direction in self.movements.keys():
            dummy_node = RopeNode(self.x, self.y)
            dummy_node.move(direction)
            min_score.append(dummy_node.get_distance_score(another_node))

        self.move(list(self.movements.keys())[min_score.index(min(min_score))])


def main():
    head = RopeNode(0, 0)
    tail = RopeNode(0, 0)
    tail_coordinate = {f'{tail.x}_{tail.y}':1}
    for line in iterate_input_file_lines(INPUT_FILE):
        direction = line.split()[0]
        step = int(line.split()[1])
        while step:
            step -= 1
            head.move(direction)
            tail.follow(head)
            tail_coordinate[f'{tail.x}_{tail.y}'] = 1
    print(sum([x for x in tail_coordinate.values()]))


if __name__=='__main__':
    main()