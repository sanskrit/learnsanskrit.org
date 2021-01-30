import glob
import os
import re

import bs4


PHP_STYLE = 'border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;'


def remove_warning(path: str) -> str:
    re_pattern = r"Failed opening '/public/vhost/l/learnsanskrit/html/include/(.*)' for"

    with open(path) as f:
        data = f.read()
    soup = bs4.BeautifulSoup(data, features='html.parser')
    divs = soup.find_all('div', {'style': PHP_STYLE})
    for div in divs:
        div_text = div.text
        if 'Failed opening' in div_text:
            match = re.search(re_pattern, div_text)
            assert match
            included_url = match.group(1)
            div.replace_with(f"{{% include 'templates/include/charts/{included_url}' %}}")
        else:
            div.decompose()

    print(f'returning: {soup}')
    return str(soup)


def main():
    for path in glob.glob(f'lso/templates/grammar/**', recursive=True):
        if os.path.isdir(path):
            continue
        out = remove_warning(path)
        with open(path, 'w') as f:
            f.write(out)


if __name__ == '__main__':
    main()
