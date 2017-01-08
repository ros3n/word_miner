import re
import nltk
from nltk.corpus import wordnet as wn
from stopwords import STOPWORDS
from graph_builder import *
import gexf_writer


def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None


def preprocess_text(text, chapters_split_re, paragraph_split_re):
    chapters = chapters_split_re.split(text.lower())[1:]
    chapters = map(lambda ch: preprocess_chapter(ch, paragraph_split_re), chapters)
    return chapters


def lemmatize_with_tag(lemmatizer, token):
    tag = nltk.pos_tag([token])
    wn_tag = penn_to_wn(tag[0][1])
    if wn_tag:
        return lemmatizer.lemmatize(token, wn_tag)
    else:
        return lemmatizer.lemmatize(token)


def preprocess_chapter(text, paragraph_split_re):
    paragraphs = paragraph_split_re.split(text)
    paragraphs = map(nltk.word_tokenize, paragraphs)
    paragraphs = [list(filter(lambda w: w not in STOPWORDS, p)) for p in paragraphs]
    paragraphs = filter(lambda p: len(p) > 1, paragraphs)
    tokens_pos = map(nltk.pos_tag, paragraphs)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatize = lambda t: lemmatize_with_tag(lemmatizer, t)
    paragraphs = [list(map(lemmatize, p)) for p in paragraphs]
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
