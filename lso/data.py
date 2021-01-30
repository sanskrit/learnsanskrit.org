from typing import Any, NamedTuple, List

class Page(NamedTuple):
    url: str
    title: str
    has_exercises: bool = False
    children: List[Any] = []


TABLE_OF_CONTENTS = [
    Page('/introduction', 'Introduction'),
    Page('/sounds', 'Sounds', children=[
        Page('/sounds/vowels', 'Vowels', children=[
            Page('/sounds/vowels/simple', 'Simple Vowels'),
            Page('/sounds/vowels/compound', 'Compound Vowels', True)]),
        Page('/sounds/consonants', 'Consonants', children=[
            Page('/sounds/consonants/stops', 'Stops and Nasals'),
            Page('/sounds/consonants/voice', 'Voice and Aspiration'),
            Page('/sounds/consonants/other', 'Other Consonants', True),
            Page('/sounds/consonants/anusvara', 'Anusvara and Visarga'),
            Page('/sounds/consonants/combinations', 'Combinations')]),
        Page('/sounds/syllables', 'Syllables'),
        Page('/sounds/reading', 'Reading'),
        Page('/sounds/review', 'Review'),
    ]),
    Page('/start', 'Starting Out', children=[
        Page('/start/verbs', 'Verb Basics', children=[
            Page('/start/verbs/present', 'Present Tense Verbs', True),
            Page('/start/verbs/roots', 'Roots and Classes', True),
            Page('/start/verbs/atmanepada', 'Atmanepada', True),
        ]),
        Page('/start/nouns', 'Noun Basics', children=[
            Page('/start/nouns/case1', 'Case 1: The Subject', True),
            Page('/start/nouns/sandhi', 'An Introduction to Sandhi', True),
            Page('/start/nouns/verbless', 'Verbless Sentences', True),
            Page('/start/nouns/pronouns', 'Pronouns', True),
            Page('/start/nouns/case2', 'Case 2: The Object', True),
            Page('/start/nouns/adjectives', 'Adjectives', True),
            Page('/start/nouns/case8', 'Case 8: Direct Address', True),
            Page('/start/nouns/neuter', 'Neuter Nouns', True),
            Page('/start/nouns/case6', 'Case 6: "of"', True),
            Page('/start/nouns/other', 'The Other Cases', True),
        ]),
        Page('/start/words', 'Making Words', children=[
            Page('/start/words/prefixes', 'Verb Prefixes', True),
            Page('/start/words/primary', 'Primary Suffixes', True),
            Page('/start/words/secondary', 'Secondary Suffixes', True),
            Page('/start/words/tatpurusha', 'The tatpurusha', True),
            Page('/start/words/asa', '"Not" and "With"', True),
        ]),
        Page('/start/uninflected', 'Uninflected Words', children=[
            Page('/start/uninflected/adverbs', 'Adverbs', True),
            Page('/start/uninflected/andornot', '"And," "Or," and "Not"', True),
            Page('/start/uninflected/emphasis', 'Adding Emphasis', True),
            Page('/start/uninflected/itiva', 'iti and iva', True),
        ]),
        Page('/start/roots', 'Gerunds and "Real" Roots', children=[
            Page('/start/roots/regular', 'Regular Roots', True),
            Page('/start/roots/gerunds', 'Gerunds', True),
            Page('/start/roots/samprasarana', 'Samprasarana', True),
            Page('/start/roots/nind', 'Roots like nind and jiv', True),
        ]),
        Page('/start/reading', 'Reading'),
        Page('/start/review', 'Review'),
    ]),
    Page('/nouns', 'Nouns', children=[
        Page('/nouns/ppp', 'The PPP', children=[
            Page('/nouns/ppp/case3', 'Case 3: "with"', True),
            Page('/nouns/ppp/passive', 'Passive Verbs', True),
            Page('/nouns/ppp/future', 'The Ordinary Future Tense', True),
            Page('/nouns/ppp/ppp', 'The PPP', True),
            Page('/nouns/ppp/vowels', 'Vowel Stems, Part 1', True),
        ]),
        Page('/nouns/compounds', 'Other Compounds', children=[
            Page('/nouns/compounds/dvandva', 'The dvandva', True),
            Page('/nouns/compounds/clauses', 'Relative Clauses', True),
            Page('/nouns/compounds/avyayibhava', 'The avyayibhava', True),
            Page('/nouns/compounds/bahuvrihi', 'The bahuvrihi', True),
        ]),
        Page('/nouns/cases', 'Three Cases', children=[
            Page('/nouns/cases/bits', 'Verb Bits', True),
            Page('/nouns/cases/case4', 'Case 4: "for"', True),
            Page('/nouns/cases/case5', 'Case 5: "from"', True),
            Page('/nouns/cases/case7', 'Case 7: "in"', True),
        ]),
        Page('/nouns/consonant', 'Consonant Stems', children=[
            Page('/nouns/consonant/one', 'One-Stem Nouns', True),
            Page('/nouns/consonant/two', 'Two-Stem Nouns', True),
            Page('/nouns/consonant/three', 'Three-Stem Nouns', True),
        ]),
        Page('/nouns/pronouns', 'More Pronouns', children=[
            Page('/nouns/pronouns/short', 'Short Pronouns, etad, and ena', True),
            Page('/nouns/pronouns/adjectives', 'Pronominal Adjectives', True),
            Page('/nouns/pronouns/questions', 'Asking Questions', True),
            Page('/nouns/pronouns/bits', 'Pronoun Bits: idam', True),
        ]),
        Page('/nouns/reading', 'Reading', children=[
            Page('/nouns/reading/pancha', 'Panchatantra'),
            Page('/nouns/reading/bg', 'Bhagavad Gita')]),
        Page('/nouns/review', 'Review'),
    ]),
    Page('/verbs', 'Verbs', children=[
        Page('/verbs/derived', 'Derived Verbs', children=[
            Page('/verbs/derived/aya', 'The -aya Class', True),
            Page('/verbs/derived/causal', 'Causal Verbs', True),
            Page('/verbs/derived/nouns', 'Verbs From Nouns', True),
            Page('/verbs/derived/prefixes', 'Noun Prefixes', True),
        ]),
        Page('/verbs/participles', 'Other Participles', children=[
            Page('/verbs/participles/present', 'Present Participles', True),
            Page('/verbs/participles/future', 'Future Participles', True),
            Page('/verbs/participles/past', 'Past Participles', True),
        ]),
        Page('/verbs/classes', 'Verb Classes', children=[
            Page('/verbs/classes/complex', 'Complex Classes', True),
            Page('/verbs/classes/past', 'The Ordinary Past Tense', True),
            Page('/verbs/classes/option', 'The Option Mood', True),
            Page('/verbs/classes/command', 'The Command Mood', True),
        ]),
        Page('/verbs/nouns', 'Vowel Nouns, Part 2', children=[
            Page('/verbs/nouns/aiu', '-a, -i, and -u Nouns', True),
            Page('/verbs/nouns/iu', '-i and -u Nouns', True),
            Page('/verbs/nouns/r', '-ṛ Nouns', True),
        ]),
        Page('/verbs/roots', 'Verb Roots', children=[
            Page('/verbs/roots/infinitives', 'Infinitives', True),
            Page('/verbs/roots/conditional', 'Conditional Verbs', True),
            Page('/verbs/roots/distant', 'The Distant Future Tense', True),
        ]),
        Page('/verbs/doubling', 'Doubling', children=[
            Page('/verbs/doubling/rules', 'General Rules', True),
            Page('/verbs/doubling/doubling', 'Doubling Class', True),
            Page('/verbs/doubling/desiderative', 'The Desiderative', True),
            Page('/verbs/doubling/intensive', 'The Intensive'),
            Page('/verbs/doubling/distant-1', 'Distant Past Tense Verbs'),
            Page('/verbs/doubling/distant-2', 'Distant Past Tense 2: Irregular Verbs'),
            Page('/verbs/doubling/distant-3', 'Distant Past Tense 3: vid and ah')
        ]),
    ]),
    Page('/ends', 'Odds and Ends', children=[
        Page('/ends/verbs', 'Verbs and Participles', children=[
            Page('/ends/verbs/three', 'Three Missing Endings', True),
            Page('/ends/verbs/recent', 'The Recent Past Tense', True),
            Page('/ends/verbs/benedictive', 'The Benedictive', True),
            Page('/ends/verbs/perfect', 'Perfect Participles', True),
            Page('/ends/verbs/prefixes', 'Separable Verb Prefixes')
        ]),
        Page('/ends/sounds', 'Sounds', children=[
            Page('/ends/sounds/l', 'ḷ and ḻ'),
            Page('/ends/sounds/accent', 'Vedic Accent'),
        ]),
        Page('/ends/nouns', 'Nouns', children=[
            Page('/ends/nouns/aioau', '-ai, -o, and -au Nouns', True),
            Page('/ends/nouns/idam', 'More on idam', True),
            Page('/ends/nouns/adas', 'adas', True),
        ]),
        Page('/ends/numbers', 'Numbers', children=[
            Page('/ends/numbers/one', 'One to One Hundred', True),
            Page('/ends/numbers/first', 'First, Second, etc.'),
            Page('/ends/numbers/use', 'Using Numbers'),
            Page('/ends/numbers/big', 'Big Numbers')
        ]),
        Page('/ends/reading', 'Reading: The Purusha Sukta'),
    ]),
    Page('/references', 'References', children=[
        Page('/references/lists', 'Lists', children=[
            Page('/references/lists/terms', 'Grammatical Terms'),
            Page('/references/lists/prefixes', 'Prefixes'),
            Page('/references/lists/primary', 'Primary Suffixes'),
            Page('/references/lists/secondary', 'Secondary Suffixes'),
            Page('/references/lists/vocabulary', 'Vocabulary')]),
        Page('/references/devanagari', 'Devanagari', children=[
            Page('/references/devanagari/letters', 'Letters and Vowel Marks'),
            Page('/references/devanagari/numbers', 'Numbers in Devanagari'),
            Page('/references/devanagari/conjunct', 'Conjunct Consonants'),
            Page('/references/devanagari/vedic', 'Basic Vedic Devanagari'),
            Page('/references/devanagari/old', 'Old Devanagari')]),
        Page('/references/nouns', 'Nouns', children=[
            Page('/references/nouns/vowels', 'Vowel Nouns'),
            Page('/references/nouns/consonants', 'Consonant Nouns'),
            Page('/references/nouns/pronouns', 'Pronouns')]),
        Page('/references/verbs', 'Verbs', children=[
            Page('/references/verbs/simple', 'Simple Verb Classes'),
            Page('/references/verbs/complex', 'Complex Verb Classes')]),
        Page('/references/sandhi', 'Sandhi', children=[
            Page('/references/sandhi/vowel', 'Vowel Sandhi'),
            Page('/references/sandhi/internal', 'Internal Consonant Sandhi'),
            Page('/references/sandhi/external', 'External Consonant Sandhi'),
            Page('/references/sandhi/visarga', 'Visarga Sandhi')]),
    ]),
]
