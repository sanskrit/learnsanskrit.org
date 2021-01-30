"""Recursively crawl learnsanskrit.org and download it as a static site."""

import logging
import os
import re

import bs4
import requests

CUR_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(CUR_DIR, 'snapshot')
ROOT = 'https://learnsanskrit.org'


def is_text(url):
    name, ext = os.path.splitext(url)
    return not ext or ext in ('.html', '.htm', '.css', '.scss', '.js', '.org')


def is_html(url):
    name, ext = os.path.splitext(url)
    return not ext or ext in ('.html', '.htm', '.org')


def url_to_filepath(url):
    if url.startswith('/'):
        path = url
    elif 'learnsanskrit.org' in url:
        _, _, path = url.partition('learnsanskrit.org/')
    else:
        return None

    # Remove all leading slashes, e.g. if accidentally doubled up
    while path.startswith('/'):
        _, _, path = path.partition('/')

    if is_html(url):
        return os.path.join(OUTPUT_DIR, path, 'index.html')
    return os.path.join(OUTPUT_DIR, path)
assert '/learnsanskrit.org/snapshot/index.html' in url_to_filepath(ROOT)


def fetch_and_write(url: str):
    if url.startswith('/'):
        url = ROOT + url
        log.warning(f'Using amended URL: "{url}"')
    log.warning(f'Fetching: "{url}"')
    r = requests.get(url)
    if r.status_code != 200:
        log.warning(f'Skipping {url} with code {r.status_code}')
        return

    filepath = url_to_filepath(url)
    if not filepath:
        log.warning(f'Failed to create filepath for URL {url}')
        return

    log.warning(f'Writing {url} to filepath {filepath}')

    assert filepath.startswith(OUTPUT_DIR)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    if is_text(filepath):
        with open(filepath, 'w') as f:
            f.write(r.text)
    else:
        with open(filepath, 'wb') as f:
            f.write(r.content)
    log.warning(f'Wrote {url} to filepath {filepath}')


def extract_urls(filepath: str):
    with open(filepath) as f:
        data = f.read()
    soup = bs4.BeautifulSoup(data, features='html.parser')

    # href
    for link in soup.findAll(['a', 'link'],
            attrs={'href': re.compile("(^/)|(learnsanskrit.org)")}):
        yield link.get('href')
    for link in soup.findAll(['audio', 'img', 'script'],
            attrs={'src': re.compile("(^/)|(learnsanskrit.org)")}):
        yield link.get('src')


log = logging.getLogger(__name__)


def crawl(root):
    stack = [root]
    seen = set()

    log.warning('Starting crawl.')
    while stack:
        url = stack.pop()
        log.warning(f'Current URL: {url}')

        if url in seen:
            log.warning(f'URL has already been queried, skipping: "{url}"')
            continue
        seen.add(url)

        filepath = url_to_filepath(url)
        if os.path.exists(filepath):
            log.warning(f'URL is already on disk (skip network call): "{url}"')
        else:
            fetch_and_write(url)

        if not os.path.exists(filepath):
            log.warning('Missing filepath, skipping: {filepath}')
            continue

        if is_html(url):
            log.warning(f'Extending with links from filepath "{filepath}"')
            stack.extend(extract_urls(filepath))
    log.warning('Complete.')


crawl(ROOT)
