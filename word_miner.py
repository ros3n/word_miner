import re

import networkx as nx

from preprocessor import preprocess_text
from graph_builder import build_graph, add_graph_to_dynamic_graph

def process_text(text, chapters_split_re, paragraph_split_re):
    chapters = preprocess_text(text, chapters_split_re, paragraph_split_re)
    res_g = nx.MultiGraph(mode='dynamic')
    for i, chapter in enumerate(chapters):
        g = build_graph(chapter)
        res_g = add_graph_to_dynamic_graph(res_g, g, i)
    return res_g


def texts():
    return {
        'Christie': {
            'The Mysterious Affair at Styles': (
                '/Users/rafal/Desktop/christie.txt',
                'chapter\s\w+\.\s.+\n',
                '\n\n'
            )
        },
        'Caroll': {
            'Alice in Wonderland': (
                '/Users/rafal/Desktop/alice.txt',
                'chapter\s\w+\n+\[sidenote:\s.+?\]\n',
                '\n\n'
            )
        }
    }


if __name__ == '__main__':
    # author_name = 'Christie'
    # book_title = 'The Mysterious Affair at Styles'
    author_name = 'Caroll'
    book_title = 'Alice in Wonderland'
    book_data = texts()[author_name][book_title]
    with open(book_data[0]) as f:
        text = f.read()
    chapters_split_re = re.compile(book_data[1], re.M)
    paragraph_split_re = re.compile(book_data[2], re.M)
    res = process_text(text, chapters_split_re, paragraph_split_re)
    nx.write_gexf(res, '{0}.gexf'.format(book_title))
