import json
import urllib, urllib2

API_URL = 'http://wolnelektury.pl/api'
WL_URL = 'http://wolnelektury.pl'
AUTHORS_PATH = 'authors'
BOOKS_PATH = 'books'
NOVELS_PATH = 'kinds/epika'
BOOK_PATH = 'media/book/txt'

def authors():
    url = '/'.join((API_URL, AUTHORS_PATH))
    data = get(url)
    if data:
        return data
    else:
        return []

def books(author_slug):
    url = '/'.join((API_URL, AUTHORS_PATH, author_slug, NOVELS_PATH, BOOKS_PATH))
    data = get(url)
    if data:
        return data
    else:
        return []

def book(book_slug):
    book_slug = '{0}.txt'.format(book_slug)
    url = '/'.join((WL_URL, BOOK_PATH, book_slug))
    try:
        response = urllib2.urlopen(url).read()
        return response
    except urllib2.HTTPError:
        print 'HTTPError for url: {0}'.format(url)
        return ''

def get(url):
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        return data
    except urllib2.HTTPError:
        print 'HTTPError for url: {0}'.format(url)
        return None
