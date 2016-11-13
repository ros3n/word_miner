import json
import urllib, urllib2

API_URL = 'http://wolnelektury.pl/api'
AUTHORS_PATH = 'authors'
BOOKS_PATH = 'books'
NOVELS_PATH = 'kinds/epika'

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

def get(url):
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        return data
    except urllib2.HTTPError:
        return None
