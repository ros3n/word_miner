import itertools
import networkx as nx


def build_graph(chapter):
    g = nx.Graph()
    for p in chapter:
        add_paragraph_weights(g, p)
    return g


def add_paragraph_weights(graph, paragraph):
    for a, b in ngrams(paragraph, 2):
        increase_edge_weight(graph, a, b)
    for words in ngrams(paragraph, 5):
        for a, b in itertools.combinations(words, 2):
            increase_edge_weight(graph, a, b)


def ngrams(l, n):
    return zip(*[l[i:] for i in range(n)])


def increase_edge_weight(graph, a, b):
    if graph.has_edge(a, b):
        graph[a][b]['weight'] += 1
    else:
        graph.add_edge(a, b, weight=1)
    return graph


def add_spells_to_node(graph, n, spells):
    if graph.node[n].get('spells'):
        graph.node[n]['spells'].extend(spells)
    else:
        graph.node[n]['spells'] = spells
    return graph


def edges_to_csv_format(graph):
    get_weight = lambda x: graph.get_edge_data(x[0], x[1])['weight']
    edges = [
        '{0},{1},{2}'.format(e[0], e[1], get_weight(e)) for e in graph.edges()
    ]
    return edges


def save_graph_to_file(graph, filename, chapter_id):
    with open(filename, 'w') as ef:
        ef.write('Source,Target,Weight,Type,Start\n')
        for edge in edges_to_csv_format(graph):
            ef.write(edge + ',Undirected,{0}\n'.format(chapter_id))


def dynamic_edges_to_csv_format(graph):
    get_attr = lambda x, index, key: graph.get_edge_data(x[0], x[1])[index][key]
    get_weight = lambda x, index: get_attr(x, index, 'weight')
    get_timestamp = lambda x, index: get_attr(x, index, 'timestamp')
    edges = []
    for e in graph.edges():
        for ts in graph.get_edge_data(e[0], e[1]).keys():
            edges.append(
                '{0},{1},{2},{3}'.format(
                    e[0], e[1], get_weight(e, ts), get_timestamp(e, ts)
                )
            )
    return edges


def save_dynamic_graph_to_file(graph, filename):
    with open(filename, 'w') as ef:
        ef.write('Source,Target,Weight,Timestamp,Type\n')
        for edge in dynamic_edges_to_csv_format(graph):
            ef.write(edge + ',Undirected\n')
