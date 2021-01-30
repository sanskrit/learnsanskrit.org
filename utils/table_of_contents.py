"""Extracts grammar structure from legacy grammar page."""

import bs4


grammar = 'lso/templates/grammar/index.html'

with open(grammar) as f:
    data = f.read()


soup = bs4.BeautifulSoup(data, features='html.parser')
for a in soup.find('ul', {'class': 'contents'}).find_all('a'):
    print(a.get('href'), a.text)
