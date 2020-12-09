import json
import argparse

'''
graph format and example modified from https://www.python.org/doc/essays/graphs/.
We use dictionary of nodes to represent a graph. Example:
    graph = {'A': ['+', ['B', 'C'] ],
             'B': ['*', ['C', 'D'] ],
             'C': ['and', ['D'] ],
             'D': ['+', ['C'] ],
             'E': ['and', ['F'] ],
             'F': ['or', ['C'] ]}
'''

example_graph =  {'A': ['+', ['B', 'C'] ], 'B': ['*', ['A', 'C', 'D'] ], 'C': ['and', ['A','B','D'] ],             'D': ['+', ['B','C'] ], 'E': ['and', ['F'] ], 'F': ['or', ['E', 'C'] ]}


def process_commands():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', '--graph_file_path', default='./mico.lg',help='the file path of the input graph')
    
    parser.add_argument('-ex', '--example', action='store_true', help='whether to use the example graph to test the analyzer')  
    
    parser.add_argument('-d', '--depth', default = 3, type=int, help='the depth of the graph pattern we want to analyze')
    parser.add_argument('-t', '--top_frequency', default = 5, type=int, help='number of the top patterns sorted by their frequency')

    return parser.parse_args()


def read_graph_from_file(graph_filepath):
    with open(graph_filepath, 'r') as fin:
        graph = {}
        lines = fin.readlines()
        for line in lines[1:]:
            t = line.split(' ')
            v_e = t[0]
            if v_e == 'v':
                node = t[1]
                type = t[2].strip()
                graph[node] = [type,[]]
            elif v_e == 'e':
                node1 = t[1]
                node2 = t[2]
                graph[node1][1].append(node2)
                graph[node2][1].append(node1)
    return graph
    
def read_graph_from_file_bak(graph_filepath):
    with open(graph_filepath, 'r') as fin:
        graph = {}
        lines = fin.readlines()
        pattern_dict = {}
        for line in lines[1:]:
            t = line.split(' ')
            v_e = t[0]
            if v_e == 'v':
                node = t[1]
                type = t[2].strip()
                graph[node] = [type,[]]
            elif v_e == 'e':
                node1 = t[1]
                node2 = t[2]
                type1 = graph[node1][0]
                type2 = graph[node2][0]
                if int(type1) <= int(type2):
                    pattern = {0:[type1, [1]], 1:[type2, [0]]}
                else:
                    pattern = {0:[type2, [1]], 1:[type1, [0]]}
                pattern = json.dumps(pattern)
                if pattern in pattern_dict:
                    pattern_dict[pattern] += 1
                else:
                    pattern_dict[pattern] = 1
    return pattern_dict


def node_set_to_pattern(node_set, graph):
    #print(node_set)
    #node_type_list = []
    #for node in node_set:
    #    node_type_list.append([node, graph[node][0]])
    #for node_type in node_type_list:
    #    print(node_type)
    #sorted_node_type_list = sorted(node_type_list, key=lambda x:x[1] )
    #print(sorted_node_type_list)
    #for i in sorted_node_type_list:
    #    print(i)
    #sorted_node_list = [x[0] for x in sorted_node_type_list]
    #print(sorted_node_list)
    #print(node_set)
    #if len(node_set) == 1:
    #    sorted_node_list = list(node_set)
    #    print('hi')
    #else:
    sorted_node_list = sorted(node_set, key=lambda x:graph[x][1] )
    #for i in sorted_node_list:
    #    print(i)
    node_id = 0
    id_dict = {}
    pattern = {}
    for node in sorted_node_list:
        id_dict[node] = node_id
        node_id += 1
    for node in sorted_node_list:
        node_type = graph[node][0]
        neibor_nodes = graph[node][1]
        new_node = {id_dict[node]:[ node_type, [] ]}
        for n_node in neibor_nodes:
            if n_node in id_dict:
                new_node[ id_dict[node] ][1].append(id_dict[n_node])
            new_node[ id_dict[node] ][1] = sorted(new_node[ id_dict[node] ][1])
        pattern[ id_dict[node] ] = new_node[id_dict[node] ]
        
    return json.dumps(pattern)
        


def get_pattern_depth_dict(graph, depth):
    pattern_depth_dict = {}
    node_sets_dict = {}
    #a graph pattern is a subgraph where the node identifier is based the sorted results of their node types
    current_pattern = {}
    for dth in range(depth):
        pattern_dict = {}
        checked_node_sets = []
        if dth == 0:
            for node in graph:
                pattern = node_set_to_pattern(set([node]), graph)
                if pattern in pattern_dict:
                    pattern_dict[pattern] += 1
                else:
                    pattern_dict[pattern] = 1     
                checked_node_sets.append(set([node]))
            node_sets_dict[dth] = checked_node_sets
                
        if dth != 0:
            count = 0
            previous_node_sets = node_sets_dict[dth-1]
            #print(dth, previous_node_sets)
            for previous_node_set in previous_node_sets:
                for node in previous_node_set:
                    neibor_nodes = graph[node][1]
                    for n_node in neibor_nodes:
                        if n_node in previous_node_set:
                            continue
                        node_set = previous_node_set.copy()
                        node_set.add(n_node)
                        if node_set in checked_node_sets:
                            continue
                        else:
                            #print('node set:', node_set)
                            pattern = node_set_to_pattern(node_set, graph)
                            if pattern in pattern_dict:
                                pattern_dict[pattern] += 1
                            else:
                                pattern_dict[pattern] = 1
                            checked_node_sets.append(node_set)
            node_sets_dict[dth] = checked_node_sets
        pattern_depth_dict[dth+1] = pattern_dict
    
    return pattern_depth_dict

def get_graph_pattern_bak(graph, depth):
    pattern_dict = {}
    now_depth = 0
    for node in graph:
        node_type = graph[node][0]
        neibor_nodes = graph[node][1]
        #a graph pattern is a subgraph where the node identifier is based the sorted results of their node types
        pattern = { 0:[ node_type,[] ] }
        if depth == 1:
            if pattern in pattern_dict:
                pattern_dict[pattern] += 1
            else:
                pattern_dict[pattern] = 1
        else:
            for n_node in neibor_nodes:
                neibor_node = graph[n_node]
                
def print_pattern_statistics(pattern_depth_dict, depth, n_top_patterns):
    for dth in range(depth):
        dth += 1
        print("for depth ", dth)
        pattern_dict = pattern_depth_dict[dth]
        sorted_pattern = sorted(pattern_dict.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_pattern) > n_top_patterns:
            sorted_pattern = sorted_pattern[:n_top_patterns]
        for pattern in sorted_pattern:
            print("pattern: ", pattern[0])
            print("frequency: ", pattern[1])
    
def main():
    args = process_commands()
    if args.example:
        graph = example_graph
    else:
        graph = read_graph_from_file(args.graph_file_path)
    
    triverse_depth = args.depth
    n_top_patterns = args.top_frequency

    pattern_depth_dict = get_pattern_depth_dict(graph, triverse_depth)
    print_pattern_statistics(pattern_depth_dict, triverse_depth, n_top_patterns)

    

if __name__ == "__main__":
    main()