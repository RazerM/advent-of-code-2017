import networkx as nx

groups = dict()
graph = nx.Graph()

with open('../input/12.txt') as fp:
    for line in fp:
        program, connected = line.strip().split(' <-> ')
        program = int(program)
        connected = (int(x) for x in connected.split(', '))
        graph.add_edges_from((program, c) for c in connected)


print('Part 1:', len(nx.single_source_shortest_path(graph, 0)))
print('Part 2:', nx.number_connected_components(graph))
