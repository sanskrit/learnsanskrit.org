import re


vargas = [
    "kKgGN",
    "cCjJY",
    "wWqQR",
    "tTdDn",
    "pPbBm",
]


def anusvara_parasavarna(match) -> str:
    next = match.group(0)[1]
    for varga in vargas:
        if next in varga:
            return varga[-1] + next


def normalize_key(s: str) -> str:
    """Normalize word spellings.

    - apply parasavarNatva
    - (todo?) reduce consonant clusters, e.g. vArttika > vArtika
    - (todo?) simplify final consonants, e.g. kakubh > kakup

    """
    pattern = "M[{}]".format("".join(vargas))
    text = re.sub(pattern, anusvara_parasavarna, s)

    return text
    # Hackily fix common doubles
    # text = text.replace('rtt', 'rt')
    # return text.replace('ttr', 'tr')
