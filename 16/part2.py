import itertools
INPUT_FILE = r'input.txt'

def iterate_file(input_file=INPUT_FILE):
    with open(input_file, 'r') as f:
        for line in f:
            yield line.strip()

def get_parsed_input(input_file=INPUT_FILE):
    valve_dict = {}
    starting_node = None
    for line in iterate_file(input_file):
        tokens = line.split()
        valve_source = tokens[1]
        flow_rate = int(tokens[4].split('=')[-1].replace(';', ''))
        valve_destination = [x.strip().replace(',','') for x in tokens[9:]]
        valve_dict[valve_source] = [flow_rate, valve_destination]
        if starting_node is None:
            starting_node = valve_source
    return starting_node, valve_dict

def dijkstra(g, starting_node):
    unvisited_node = set([x for x in g.keys()])
    shortest_path = {x:float('inf') for x in unvisited_node}
    shortest_path[starting_node] = 0
    adj_node = {}
    adj_node[starting_node] = None

    while unvisited_node:

        min_node = None
        min_path = None
        for node in unvisited_node:
            path = shortest_path[node]
            if min_node is None:
                min_node, min_path = node, path
                continue
            if path < min_path:
                min_node, min_path = node, path

        for neighbor_node in g[min_node]:
            temp_path = shortest_path[min_node] + 1
            if temp_path < shortest_path[neighbor_node]:
                shortest_path[neighbor_node] = temp_path
                adj_node[neighbor_node] = min_node

        unvisited_node.remove(min_node)

    return shortest_path, adj_node

def sort_dict(data:dict):
    data = dict(data)
    sorted_data = sorted(data.items(), key=lambda x:x[1], reverse=True)
    return {key:value for key, value in sorted_data}

def main():
    starting_node, valve_dict = get_parsed_input()
    total_minute = 26
    valve_graph = {key:value[1] for key, value in valve_dict.items()}
    flow_rate = {key:value[0] for key, value in valve_dict.items()}
    path_distances = {v:dijkstra(valve_graph, v)[0] for v in valve_graph.keys()}
    non_zero_valves = [node for node in valve_dict.keys() if valve_dict[node][0]]
    sim_eff = lambda v, r, sn: [(r - (path_distances[sn][v[0]]+1))*flow_rate[v[0]], r - (path_distances[sn][v[0]]+1), v[0]]

    score_points = {'':[0, total_minute, 'AA']}
    pos_comb = {}
    

    current_max_score = 0
    total_valve_count = len(non_zero_valves)
    top_n_list = None
    for v in range(total_valve_count):
        if top_n_list is None:
            top_n_list_keys = [[] for _ in range(total_valve_count)]
        else:
            top_n_list_keys = [key.split('_') for key in top_n_list.keys()]
        new_top_n_list = {}
        print(v, len(top_n_list_keys))
        
        for key in top_n_list_keys:
            base_key = '_'.join(key)
            base_score, base_r, base_sn = score_points[base_key]
            for n_valve in [x for x in non_zero_valves if x not in key]:
                new_list_key = '_'.join([base_key,n_valve])
                score_points[new_list_key] = list(sim_eff([n_valve], base_r, base_sn))
                score_points[new_list_key][0] += base_score
                score = score_points[new_list_key][0]
                current_max_score = max(score, current_max_score)
                r = score_points[new_list_key][1]

                min_path_distance = min([path_distances[n_valve][x] for x in non_zero_valves if x not in new_list_key[1:].split('_')])
                if min_path_distance + 1> r:
                    pos_comb_key = '_'.join(new_list_key.split('_')[1:])
                    pos_comb[pos_comb_key] = score
                    continue

                new_top_n_list[new_list_key] = score
            
        if len(new_top_n_list) == 0:
            break
        top_n_list = sort_dict(new_top_n_list)

    def is_overlapping(list1, list2):
        for x in list1:
            if x in list2:
                return True
        return False

    max_score = 0
    N = 10000
    pos_comb = sort_dict(pos_comb)
    pos_comb = [[k, v] for k, v in pos_comb.items()]

    for key1, value1 in pos_comb:
        if 2*value1 < max_score:
            break
        for key2, value2 in [[k,v] for k,v in pos_comb if value1+v > max_score]:
            if is_overlapping(key1.split('_'), key2.split('_')):
                continue
            score = value1 + value2
            if score > max_score:
                max_score = score
                print(key1, value1, key2, value2, max_score)


if __name__=='__main__':
    main()