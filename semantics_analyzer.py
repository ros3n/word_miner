
# -*- encoding: utf-8 -*-

from collections import Counter, defaultdict
from operator import itemgetter
from pickle import load
import re
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book

BETA = 0.00002
GAMMA = 0.00002
ALPHA = 0.66

class SemanticsAnalyser():
    def __init__(self, book, beta=BETA, gamma=GAMMA, alpha=ALPHA):
        self.book = book
        self.filtered_files = []
        self.beta = beta
        self.gamma = gamma
        self.Q = 0.0
        self.H = Counter()
        self.alpha = alpha
        self.H_neigh = defaultdict(lambda: Counter())
        self.r = defaultdict(lambda: Counter())

    def preprocess(self):
        self.preprocess_contents()
        for index, word in enumerate(self.book_words):
            self.H[word] += 1
            self.Q += 1

    def count_frequencies(self):
        l = len(self.book_words)
        for index, key in enumerate(self.book_words):
            # if key in self.keywords:
            b = max(0, index - 12)
            p = max(0, index - 1)
            p2 = min(l - 1, index + 1)
            e = min(index + 12, l - 1)
            for neigh in self.book_words[b:p] + self.book_words[p2:e]:
                self.H_neigh[key][neigh] += 1

    def construct_r(self):
        for i, j_dict in self.H_neigh.items():
            r = Counter()
            for j, h_i_j in j_dict.items():
                h_j = self.H[j]
                if h_j > self.beta * self.Q:
                    r[j] = (h_i_j / self.Q) / ((h_j / self.Q) ** self.alpha)
                else:
                    r[j] = (h_i_j/self.Q) / (self.gamma * self.Q)
            self.r[i] = r

    def print_correlations(self, n):
        for word in self.book_words:
            print(word)
            print(sorted(self.r[word].items(), key=itemgetter(1), reverse=True)[:n])
            print()

    def preprocess_contents(self):
        data = self.book.contents.lower()
        data = re.sub(r'[\.|,|-|_|!|?|;|"|\(|\)]', ' ', data)
        data = re.sub(r'[^a-z|ą|ć|ę|ł|ń|ó|ś|ż|ź|\n|\s]', '', data)
        data = re.sub(r'\n+', ' ', data)
        data = re.sub(r'\s+', ' ', data)
        self.book_words = data.split()
        return self.book_words


if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    # book = s.query(Book).first()
    book = s.query(Book).get(1318)
    sa = SemanticsAnalyser(book)
    sa.preprocess()
    # print(sa.book_words[:100])
    sa.count_frequencies()
    sa.construct_r()
    sa.print_correlations(5)
