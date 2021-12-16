from copy import deepcopy
import heapq as heap
from collections import defaultdict

def main():
    with open('data/day15.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    risk = [[int(ci) for ci in c] for c in contents]

    # Puzzle 1
    risk = build_large_map(risk, 1)
    graph = build_graph(risk)
    _, shortest_paths_nodes = dijikstra(graph, (0,0))
    asw1 = shortest_paths_nodes[(len(risk) - 1, len(risk[0]) - 1)]
    print(f'(Puzzle 1) Lowest path risk: {asw1}')

    # Puzzle 2
    risk = build_large_map(risk, 5)
    graph = build_graph(risk)
    _, shortest_paths_nodes = dijikstra(graph, (0,0))
    asw2 = shortest_paths_nodes[(len(risk) - 1, len(risk[0]) - 1)]
    print(f'(Puzzle 2) Lowest path risk after 5 extensions: {asw2}')



def build_graph(risk):
    """ Builds graph dictionary from risk map """
    h, w = len(risk), len(risk[0])
    steps = [[0, -1], [1, 0], [-1, 0], [0, 1]]
    graph = dict()
    for r in range(h):
        for c in range(w):
            dirs = [[r + x, c + y] for x, y in steps]
            for (d1, d2) in dirs:
                if (d1 < 0) or (d2 < 0) or (d1 == h) or (d2 == w):
                    dirs.remove([d1, d2])
            if r == (h-1) and c == 0:
                dirs.remove([h, 0])
            if r == 0 and c == (w-1):
                dirs.remove([0, w])

            graph[(r,c)] = {(i,j):risk[i][j] for (i, j) in dirs}
    return graph


def dijikstra(graph, start = (0,0)):
    """
    Returns optimal path as previous-node dictionary and the costs in node
    using the dijikstra algorithm
    """
    verts = set(graph.keys())
    shortest_dist = defaultdict(lambda: float('inf'))
    shortest_dist[start] = 0
    previous_vertex = dict()
    visited = set()

    pq = []
    heap.heappush(pq, (0, start))

    while pq:
        _, node = heap.heappop(pq)

        for neigh, cost in graph[node].items():
            if neigh in visited:
                continue
            r, c = neigh
            distance = shortest_dist[node] + cost
            if  distance < shortest_dist[neigh]:
                previous_vertex[neigh] = node
                shortest_dist[neigh] = distance
                heap.heappush(pq, (distance, neigh))

        visited.add(node)

    return previous_vertex, shortest_dist


def build_large_map(risk, n=5):
    """ Builds larger risk map with n extensions according to function `val` """
    h, w = n*len(risk), n*len(risk[0])
    out = []
    for r in range(h):
        out_sub = []
        for c in range(w):
            out_sub.append(val(risk, r, c))
        out.append(out_sub)
    return out


def val(risk, r, c):
    h, w = len(risk), len(risk[0])
    row, col = r % h, c % w
    n, m = r // h, c // w
    shift = lambda x, s: ((x + s - 1) % 9 + 1)
    return shift(shift(risk[row][col], n), m)


def lowest_risk_expansion(risk, n_exps = 5):
    """
    Returns lowest risk for any path when the map is extended if
    movments allowed are only down or right
    """
    h, w = n_exps * len(risk), n_exps * len(risk[0])
    total_costs = []
    for r in range(h):
        total_costs_row = []
        for c in range(w):
            if (c == 0) and (r == 0):
                total_costs_row.append(0)
            elif c == 0 and r > 0:
                total_costs_row.append(total_costs[r-1][c] + val(risk, r, c))
            elif c > 0  and r == 0:
                total_costs_row.append(total_costs_row[c-1] + val(risk, r, c))
            else:
                total_costs_row.append(min(total_costs_row[c-1],
                                           total_costs[r-1][c]) + val(risk, r, c))

        total_costs.append(total_costs_row)

    return total_costs[-1][-1]


def lowest_risk(risk):
    """
    Returns lowest risk for any path when movments allowed are only down or right
    """
    total_costs = deepcopy(risk)

    for r, row in enumerate(risk):
        for c, val in enumerate(row):
            if (c == 0) and (r == 0):
                total_costs[r][c] = 0
            elif c == 0 and r > 0:
                total_costs[r][c] = total_costs[r-1][c] + risk[r][c]
            elif c > 0  and r == 0:
                total_costs[r][c] = total_costs[r][c-1] + risk[r][c]
            else:
                total_costs[r][c] = min(total_costs[r][c-1], total_costs[r-1][c]) + risk[r][c]

    return total_costs[-1][-1]


if __name__ == '__main__':
    main()
