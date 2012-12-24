from sanskrit import sounds
from sanskrit.schema import Tag
from lso import ctx


class Readable(object):

    def __init__(self, ctx):
        self.ctx = ctx
        enum_abbr = ctx.enum_abbr

        gender = {
            'm': 'masc.',
            'f': 'fem.',
            'n': 'neut.',
            'none': '',
            }

        case = {
            '1': 'nom.',
            '2': 'acc.',
            '3': 'ins.',
            '4': 'dat.',
            '5': 'abl.',
            '6': 'gen.',
            '7': 'loc.',
            '8': 'voc.',
            }

        number = {
            's': 'sg.',
            'd': 'du.',
            'p': 'pl.'
            }

        person = {
            '1': '1st.',
            '2': '2nd.',
            '3': '3rd.',
            }

        mode = {
            'pres': 'present',
            'ipft': 'imperfect',
            'impv': 'imperative',
            'opt': 'optative',
            'cond': 'conditional',
            'sfut': 'near future',
            'aor': 'aorist',
            'inj': 'injunctive',
            'perf': 'perfect',
            'ben': 'benedictive',
            'dfut': 'distant future',
            }

        voice = {
            'P': 'P.',
            'A': 'A',
            'passive': 'passive',
            }

        self.genders = enum_abbr['gender_group']

        self.gender = self._custom_abbr(gender, 'gender')
        self.case = self._custom_abbr(case, 'case')
        self.number = self._custom_abbr(number, 'number')
        self.person = self._custom_abbr(person, 'person')
        self.mode = self._custom_abbr(mode, 'mode')
        self.voice = self._custom_abbr(voice, 'voice')

        self.verb_tmp = '{0} {1} {2} {3}'
        self.nominal_tmp = '{0} {1} {2}'

    def _custom_abbr(self, abbr, name):
        enum = self.ctx.enum_id[name]
        return {enum[k]: v for k, v in abbr.iteritems()}

    def form_abbr(self, form):
        pos_id = form.pos_id

        if pos_id in (Tag.NOUN, Tag.ADJECTIVE, Tag.PRONOUN, Tag.PARTICIPLE):
            g = self.gender[form.gender_id]
            c = self.case[form.case_id]
            n = self.number[form.number_id]
            return self.nominal_tmp.format(g, c, n)

        elif pos_id == Tag.VERB:
            p = self.person[form.person_id]
            n = self.number[form.number_id]
            m = self.mode[form.mode_id]
            v = self.voice[form.voice_id]
            return self.verb_tmp.format(p, n, m, v)

        elif pos_id == Tag.INDECLINABLE:
            return 'ind.'

        return None

    def stem_abbr(self, stem):
        pos_id = stem.pos_id
        if pos_id == Tag.NOUN:
            return '{0}.'.format(self.genders[stem.genders_id])

        elif pos_id == Tag.ADJECTIVE:
            return 'adj.'

        elif pos_id == Tag.PRONOUN:
            return 'pronoun'

        elif pos_id == Tag.PARTICIPLE:
            mode = self.mode[stem.mode_id]
            voice = self.voice[stem.mode_id]

        return '?'

    def root_abbr(self, root):
        return '(verb)'
