import re

def author_slug(author_data):
    return author_data['href'].split('/')[-2]

def author_name(author_data):
    return author_data['name']
