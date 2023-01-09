INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')


class Node:

    def __init__(self, i, j, letter_value):
        self.i = i
        self.j = j
        self.elevation = self.calculate_elevation(letter_value)
        self.neighbor_keys = []

    def get_neighbor_keys(self):
        return self.neighbor_keys
    
    def calculate_elevation(self, letter):
        if letter=='S':
            return self.calculate_elevation('a')
        if letter=='E':
            return self.calculate_elevation('z')
        return list('abcdefghijklmnopqrstuvwxyz').index(letter)

    def get_key(self):
        return f'{self.i}_{self.j}'
    
    def get_distance(self, neighbor_key):
        return 1
    
    def set_neighbor_keys(self, neighbor_keys):
        self.neighbor_keys = neighbor_keys


class Graph:

    def __init__(self, raw_values):
        self.nodes = {}
        self.init_nodes(raw_values)
        self.init_node_neighbors()
    
    def init_nodes(self, raw_values):
        for i, line in enumerate(raw_values):
            for j, item in enumerate(line):
                node = Node(i, j, item)
                self.nodes[node.get_key()] = node
    
    def init_node_neighbors(self):
        node_keys = self.get_node_keys()
        for node in self.nodes.values():
            neighbor_keys = []
            for n_key in [f'{node.i+x}_{node.j+y}' for x,y in [(1,0), (0,-1), (-1,0), (0,1)]]:
                if n_key not in node_keys:
                    continue
                if not self.is_route_available(node, self.get_node(n_key)):
                # if self.get_node(n_key).elevation < node.elevation - 1:
                    continue
                neighbor_keys.append(n_key)
            node.set_neighbor_keys(neighbor_keys)
    
    def is_route_available(self, node_source, node_destination):
        return node_source.elevation >= node_destination.elevation - 1

    def get_node_keys(self):
        return [x for x in self.nodes.keys()]
    
    def get_node(self, node_key):
        return self.nodes[node_key]


def dijkstra_algorithm(graph:Graph, start_node_key, end_node_key=None):
    shortest_path = {key : float('inf') for key in graph.get_node_keys()}
    shortest_path[start_node_key] = 0.0
    
    unvisited_nodes = set([x for x in graph.get_node_keys()])

    while unvisited_nodes:

        current_node_key = min(unvisited_nodes, key=lambda x: shortest_path[x])
        current_node = graph.get_node(current_node_key)

        for neighbor_key in current_node.get_neighbor_keys():
            temp_value = shortest_path[current_node_key] + current_node.get_distance(neighbor_key)
            if temp_value < shortest_path[neighbor_key]:
                shortest_path[neighbor_key] = temp_value
        
        unvisited_nodes.remove(current_node_key)

        if end_node_key is None:
            continue

        if current_node_key==end_node_key:
            return shortest_path[current_node_key]
        
    return shortest_path


def main(input_file=INPUT_FILE):
    start_key = None
    end_key = None
    parsed_input = []
    for i, line in enumerate(iterate_input_file_lines(input_file)):
        row = []
        for j, item in enumerate(line):
            row.append(item)
            if item == 'S':
                start_key = f'{i}_{j}'
            if item == 'E':
                end_key = f'{i}_{j}'
        parsed_input.append(row)

    print(dijkstra_algorithm(Graph(parsed_input), start_key, end_key))


if __name__=='__main__':
    main()