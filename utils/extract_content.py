import glob
import os

import bs4


SNAPSHOT_DIR = 'snapshot'
OUTPUT_DIR = 'templates/grammar'


def extract_and_move(raw_file, out_file):
    with open(raw_file) as f:
        data = f.read()

    soup = bs4.BeautifulSoup(data, features='html.parser')

    title = soup.find('title')
    content = soup.find(id='content')
    navigation = soup.find('div', {'class': 'bar'}).find('ul')

    title_str, _, _ = str(title.text).partition('|')
    title_str = title_str.strip()

    content.find('form').decompose()
    content_str = content.decode_contents()

    directory = os.path.dirname(out_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(out_file, 'w') as f:
        f.write("{% extends 'base-grammar.html' %}\n\n")
        f.write(f"{{% block title %}}{title_str}{{% endblock %}}\n\n")
        f.write(f"{{% block grammar_nav %}}\n{str(navigation)}\n{{% endblock %}}\n\n")
        f.write(f"{{% block content %}}{content_str}\n{{% endblock %}}\n\n")


def main():
    for directory in ['ends', 'grammar', 'introduction', 'monier', 'nouns',
            'panini', 'prosody', 'references', 'sounds', 'start', 'supp', 'verbs']:
        for input_path in glob.glob(f'{SNAPSHOT_DIR}/{directory}/**', recursive=True):
            if os.path.isdir(input_path):
                continue
            output_path = os.path.join(OUTPUT_DIR, input_path[len(SNAPSHOT_DIR)+1:])
            print(input_path, output_path)
            extract_and_move(input_path, output_path)


if __name__ == '__main__':
    main()
