from part1 import *

class GraphAdjusted(Graph):
    
    def is_route_available(self, node_source, node_destination):
        return node_destination.elevation >= node_source.elevation - 1


def main(input_file=INPUT_FILE):
    a_key_list = []
    end_key = None
    parsed_input = []
    for i, line in enumerate(iterate_input_file_lines(input_file)):
        row = []
        for j, item in enumerate(line):
            row.append(item)
            if item == 'a':
                a_key = f'{i}_{j}'
                a_key_list.append(a_key)
            if item == 'E':
                end_key = f'{i}_{j}'
        parsed_input.append(row)

    shortest_paths = dijkstra_algorithm(GraphAdjusted(parsed_input), end_key)
    print(min([shortest_paths[a_key] for a_key in a_key_list]))

if __name__=='__main__':
    main()