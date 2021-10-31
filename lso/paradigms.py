a_m = """
aH au AH
am au An
ena AbhyAm aiH
Aya AbhyAm ebhyaH
At AbhyAm ebhyaH
asya ayoH AnAm
e ayoH eSu
a au AH
"""

a_n = """
am e Ani
am e Ani
a e Ani
"""

A_f = """
A e AH
Am e AH
ayA AbhyAm AbhiH
Ayai AbhyAm AbhyaH
AyAH AbhyAm AbhyaH
AyAH ayoH AnAm
AyAm ayoH Asu
e e AH
"""

I_f = """
I yau yaH
Im yau IH
yA IbhyAm IbhiH
yai IbhyAm IbhyaH
yAH IbhyAm IbhyaH
yAH yoH InAm
yAm yoH ISu
i yau yaH
"""

U_f = """
UH vau vaH
Um vau UH
vA UbhyAm UbhiH
vai UbhyAm UbhyaH
vAH UbhyAm UbhyaH
vAH voH UnAm
vAm voH USu
u vau vaH
"""


def make_endings(ending_list):
    endings = ending_list.strip().split()
    assert len(endings) % 3 == 0
    return endings


stem_endings = ["a", "A", "i", "I", "u", "U"]
PARADIGMS = {
    "a_m": make_endings(a_m),
    "a_n": make_endings(a_n),
    "A_f": make_endings(A_f),
    "I_f": make_endings(I_f),
    "U_f": make_endings(U_f),
}


def get_endings_for_stem(stem, gender):
    for e in stem_endings:
        if stem.endswith(e):
            key = f"{e}_{gender}"
            return (e, PARADIGMS[key])
    raise KeyError(f"Not found: {stem}, {gender}")


def nominal(stem, gender):
    stem_type, endings = get_endings_for_stem(stem, gender)
    words = []
    for e in endings:
        word = stem[: -len(stem_type)] + e
        words.append(word)
    return words
