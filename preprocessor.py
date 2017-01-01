import re
import nltk
from stopwords import STOPWORDS
from graph_builder import *
import gexf_writer

def preprocess_text(text, chapters_split_re, paragraph_split_re):
    chapters = chapters_split_re.split(text.lower())[1:]
    chapters = map(lambda ch: preprocess_chapter(ch, paragraph_split_re), chapters)
    return chapters


def preprocess_chapter(text, paragraph_split_re):
    paragraphs = paragraph_split_re.split(text)
    paragraphs = map(nltk.word_tokenize, paragraphs)
    paragraphs = [list(filter(lambda w: w not in STOPWORDS, p)) for p in paragraphs]
    paragraphs = filter(lambda p: len(p) > 1, paragraphs)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    paragraphs = [list(map(lemmatizer.lemmatize, p)) for p in paragraphs]
    return paragraphs


if __name__ == '__main__':
    # text = nltk.corpus.gutenberg.raw('carroll-alice.txt')
    with open('/Users/rafal/Desktop/christie.txt') as f:
        text = f.read()
    chapters_split_re = re.compile('chapter\s\w+\.\s.+\n', re.M)
    paragraph_split_re = re.compile('\n\n', re.M)
    chapters = preprocess_text(text, chapters_split_re, paragraph_split_re)
    res_g = nx.MultiGraph(mode='dynamic')
    for i, chapter in enumerate(chapters):
        g = build_graph(chapter)
        # save_graph_to_file(g, 'christie_{0}_edges.csv'.format(i + 1), i + 1)
        for a, b in g.edges():
            weight = g[a][b]['weight']
            res_g.add_edge(a, b, Weight=[(weight, float(i+1), float(i+1))], spells=[(float(i+1), float(i+1))])
            add_spells_to_node(res_g, a, [(float(i+1), float(i+1))])
            add_spells_to_node(res_g, b, [(float(i+1), float(i+1))])
    nx.write_gexf(res_g, 'test.gexf')
