from flask.json import JSONEncoder

from lso.texts.models import Segment, Text
from lso.texts.views import Card, ChildCard
from lso.texts.lib import transform as xml_transform

class LSOJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, Segment):
            return {
                'text_id': o.text_id,
                'slug': o.slug,
                'content': xml_transform(o.content),
            }
        elif isinstance(o, Text):
            return {
                'id': o.id,
                'name': o.name,
                'slug': o.slug,
                'xmlid_prefix': o.xmlid_prefix
            }
        elif isinstance(o, Card):
            return {
                'primary': self.default(o.primary),
                'translations': [self.default(x) for x in o.translations],
                'commentaries': [self.default(x) for x in o.commentaries],
            }
        elif isinstance(o, ChildCard):
            return {
                'text_id': o.text_id,
                'segments': [self.default(x) for x in o.segments],
            }
        return JSONEncoder.default(self, o)
