import pytest
from lso.api.util import normalize_key


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("aMkita", "aNkita"),
        ("vidAMcakAra", "vidAYcakAra"),
        ("aMta", "anta"),
        ("saMpad", "sampad"),
        # Disabled until I decide how to handle these.
        # ('pattra', 'patra'),
        # ('vArttika', 'vArtika'),
    ],
)
def test_normalize_key(raw, expected):
    assert normalize_key(raw) == expected, normalize_key(raw)
