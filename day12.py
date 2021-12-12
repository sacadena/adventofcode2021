# https://adventofcode.com/2021/day/12
from collections import defaultdict
from copy import copy, deepcopy

def main():
    with open('data/day12.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    nodes1 = [c.split('-')[0] for c in contents]
    nodes2 = [c.split('-')[1] for c in contents]

    graph = build_graph(nodes1, nodes2)

    asw1 = count_paths('end', graph)
    print(f'(Puzzle 1) Total number of paths: {asw1}')

    asw2 = count_paths2('end', graph)
    print(f'(Puzzle 2) Total number of paths: {asw2}')

    #tempasw2 = count_paths_low_nodes_twice('end', graph)
    #print(f'Total number of paths visiting all small up to 2 times: {tempasw2}')


def count_paths2(node, graph, visited=defaultdict(int), twovisited=False):
    """ A single small cave can be visited twice """

    out_visited = deepcopy(visited)
    #out_path = copy(path)
    #out_path.append(node)

    if node == 'start':
        #print(','.join(out_path[::-1]))
        return 1

    if node.islower() and (node != 'start') and (node!= 'end'):
        out_visited[node] += 1

    if out_visited[node] == 2:
        twovisited = True

    number_visited = 0
    for child in graph[node]:
        if child == 'end':
            continue
        if twovisited and (out_visited[child] >= 1):
             continue
        number_visited += count_paths2(child, graph, out_visited, twovisited)

    return number_visited


def count_paths(node, graph, visited=set()):
    out_visited = copy(visited)
    if node == 'end' or node.islower():
        out_visited.add(node)

    if node == 'start':
        out_visited.add(node)
        return 1

    number_visited = 0
    for child in graph[node]:
        if child in out_visited:
            continue
        number_visited += count_paths(child, graph, out_visited)

    return number_visited


def count_paths_low_nodes_twice(node, graph, visited=defaultdict(int), path = []):
    """
    Small case nodes can be visited up to twice.
    Edit: This function does not solve the second puzzle. Here, all
          small nodes can be visited twice.
    """
    out_visited = deepcopy(visited)
    out_path = copy(path)
    out_path.append(node)

    if node == 'start':
        #print(','.join(out_path[::-1]))
        return 1

    if node.islower() and (node != 'start') and (node!= 'end'):
        out_visited[node] += 1

    number_visited = 0
    for child in graph[node]:
        if (out_visited[child] == 2) or (child =='end'):
            continue
        number_visited += count_paths_low_nodes_twice(child, graph, out_visited, out_path)

    return number_visited


def build_graph(nodes1, nodes2):
    graph = defaultdict(list)
    for n1, n2 in zip(nodes1, nodes2):
        graph[n1].append(n2)
        graph[n2].append(n1)

    return dict(graph)


if __name__ == '__main__':
    main()
