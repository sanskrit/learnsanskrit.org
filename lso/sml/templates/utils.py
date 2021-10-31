import re
from typing import List


def split_multiline_text(text: str) -> List[str]:
    buf = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            buf.append(line)
        else:
            if buf:
                yield "\n".join(buf)
                buf = []
    yield "\n".join(buf)
