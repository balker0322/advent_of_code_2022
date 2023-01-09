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
        # if flow_rate != 0:
        #     print(line)
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

def simulate_valve_opening(
    non_zero_valves,
    total_time,
    starting_node,
    shortest_distance,
    flow_rate,
    ):
    closed_valves = list(non_zero_valves)
    current_node = starting_node

    r = total_time
    total = 0
    while closed_valves:
        '''
        set next valve
        calc d from current to next valve
        calc remaining time
        get flow rate
        calc added pressure
        update total
        '''
        next_node= closed_valves[0]
        d = shortest_distance[current_node][next_node]
        req_t = d+1
        if req_t > r:
            break
        f = flow_rate[next_node]
        next_r = r - req_t
        points = next_r*f
        total += points
        r = next_r
        closed_valves = closed_valves[1:]
        current_node = next_node
    
    # return
    return total,r,current_node

def get_top_n(data:dict, n:int):
    data = dict(data)
    sorted_data = sorted(data.items(), key=lambda x:x[1], reverse=True)
    # if len(sorted_data) > n:
    #     return {key:value for key, value in sorted_data[:n]}
    return {key:value for key, value in sorted_data}


def main():
    starting_node, valve_dict = get_parsed_input()
    total_minute = 30
    valve_graph = {key:value[1] for key, value in valve_dict.items()}
    flow_rate = {key:value[0] for key, value in valve_dict.items()}
    path_distances = {v:dijkstra(valve_graph, v)[0] for v in valve_graph.keys()}
    non_zero_valves = [node for node in valve_dict.keys() if valve_dict[node][0]]
    # print(non_zero_valves)
    # non_zero_valves = ['DD','DD','CC','BB','BB','AA','II','JJ','JJ','II','AA','DD','EE','FF','GG','HH','HH','GG','FF','EE','EE','DD','CC','CC',]
    # non_zero_valves = ['DD','BB','JJ','HH','EE','CC',]
    sim = lambda v: simulate_valve_opening(
            v,
            total_minute,
            starting_node,
            path_distances,
            flow_rate,
        )[0]
    sim_eff = lambda v, r,sn: simulate_valve_opening(
            v,
            r,
            sn,
            path_distances,
            flow_rate,
        )
    x = sim(non_zero_valves)
    sim_eff = lambda v, r, sn: [(r - (path_distances[sn][v[0]]+1))*flow_rate[v[0]], r - (path_distances[sn][v[0]]+1), v[0]]


    # return total,r,current_node

    # return (total_time - (d+1))*f,r - (d+1),current_node

    # print(x)

    score_points = {'':[0, total_minute, 'AA']}

    # # brute force
    # max_score = 0
    # for c in itertools.permutations(non_zero_valves):
    #     x = sim(c)
    #     if x > max_score:
    #         print(c, x)
    #         max_score = x
    # print(max_score)

    N = 1000000
    current_max_score = 0
    total_valve_count = len(non_zero_valves)
    top_n_list = None
    for v in range(total_valve_count):
        if top_n_list is None:
            top_n_list_keys = [[] for _ in range(total_valve_count)]
        else:
            top_n_list_keys = [key.split('_') for key in top_n_list.keys()]
        # print(v, len(top_n_list_keys))
        new_top_n_list = {}
        
        for key in top_n_list_keys:
            base_key = '_'.join(key)
            base_score, base_r, base_sn = score_points[base_key]
            for n_valve in [x for x in non_zero_valves if x not in key]:
                # score_points = 
                # new_list = key + [n_valve]
                new_list_key = base_key+'_'+n_valve
                score_points[new_list_key] = list(sim_eff([n_valve], base_r, base_sn))
                score_points[new_list_key][0] += base_score
                score = score_points[new_list_key][0]
                # if score > current_max_score:
                #     print(new_list_key, score, score_points[new_list_key])
                current_max_score = max(score, current_max_score)
                r = score_points[new_list_key][1]
                theo_score = r*sum([flow_rate[node] for node in non_zero_valves if node not in new_list_key[1:].split('_')]) + score
                if theo_score < current_max_score:
                    continue
                new_top_n_list[new_list_key] = score
                
        top_n_list = get_top_n(new_top_n_list, N)

    print(current_max_score)
    for k,v in top_n_list.items():
        print(v, k)
        break
        # do for each item in top N as inc_seq
            # get list of all possible next item for inc_seq
                # calc score for inc_seq+next_item
    
    # max_score = 0
    # valve_count = len(non_zero_valves)
    # correct_seq = False

    # while not correct_seq:

    #     correct_seq = True
    #     s1 = sim(non_zero_valves)
    #     for i in range(valve_count-1):
    #         temp_list = list(non_zero_valves)
    #         temp_list[i], temp_list[i+1] = temp_list[i+1], temp_list[i]
    #         s1 = sim(non_zero_valves)
    #         s2 = sim(temp_list)
    #         print(s1, s2)
    #         if s2 > s1:
    #             max_score = s2
    #             print(s2)
    #             non_zero_valves = list(temp_list)
    #             correct_seq = False
    
    # print(max_score)




if __name__=='__main__':
    main()
    # data = {
    #     'a':3,
    #     'b':4,
    #     'c':6,
    #     'd':1,
    # }
    # x = get_top_n(data, 3)
    # print(x)