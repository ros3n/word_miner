import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import wl_api_utils
from wl_data_parser import *

def number_of_books(author_slug):
    print author_slug
    books = wl_api_utils.books(author_slug)
    return len(books)

def authors_by_number_of_books():
    authors = wl_api_utils.authors()
    data = map(
        lambda a: (author_name(a), slug(a), number_of_books(slug(a))),
        authors
    )
    data = [{'author': d[0], 'slug': d[1], 'book_count': d[2]} for d in data if d[2] != 0]
    with open('data/book_authors2.json', 'w') as f:
        json.dump(data, f)

def pull_authors_books(author_slug):
    book_refs = wl_api_utils.books(author_slug)
    slugs_and_titles = map(lambda x: (slug(x), book_title(x)), book_refs)
    slugs = map(lambda x: x[0], slugs_and_titles)
    titles = map(lambda x: x[1], slugs_and_titles)
    books = map(wl_api_utils.book, slugs)
    return zip(titles, books)

def store_author_and_books(author_data, session):
    author = Author(name=author_data['author'].decode('utf-8'), slug=author_data['slug'])
    books_data = pull_authors_books(author.slug)
    books = map(
        lambda x: Book(author=author, title=x[0].decode('utf-8'), contents=x[1].decode('utf-8')), books_data
    )
    session.add(author)
    map(session.add, books)
    session.commit()
    print author.name, len(books)

def populate_db():
    f = open('data/book_authors.json')
    data = json.load(f)
    f.close()
    engine = create_engine('sqlite:///db.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    map(lambda x: store_author_and_books(x, session()), data)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # authors_by_number_of_books()
    populate_db()
