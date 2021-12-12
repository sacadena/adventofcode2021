from collections import defaultdict
def main():
    with open('data/day12demo1.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    print(contents)
    #nodes1 = [c.split('-')[0] for c in contents]
    #nodes2 = [c.split('-')[1] for c in contents]

    # graph = defaultdict(list)
    # for n1, n2 in zip(nodes1, nodes2):
    #     graph[n1].append(n2)
    #     graph[n2].append(n1)
    #
    # print(graph)


if __name__ == '__main__':
    main()
