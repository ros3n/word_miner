import re

def slug(data):
    return data['href'].split('/')[-2]

def author_name(author_data):
    return author_data['name']

def book_title(book_data):
    return book_data['title']
