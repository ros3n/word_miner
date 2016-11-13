import json
import wl_api_utils
from wl_data_parser import *

def number_of_books(author_slug):
    print author_slug
    books = wl_api_utils.books(author_slug)
    return len(books)

def authors_by_number_of_books():
    authors = wl_api_utils.authors()
    data = map(
        lambda a: (author_name(a), author_slug(a), number_of_books(author_slug(a))),
        authors
    )
    data = [{'author': d[0], 'slug': d[1], 'book_count': d[2]} for d in data if d[2] != 0]
    with open('data/book_authors.json', 'w') as f:
        json.dump(data, f)

authors_by_number_of_books()
