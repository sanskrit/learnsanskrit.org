# -*- coding: utf-8 -*-
"""
    lso.lib.converters
    ~~~~~~~~~~~~~~~~~~

    Routing converters

    :license: MIT and BSD
"""
import re

from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):

    """Converter for list data. Empty entries are ignored."""

    def to_python(self, s):
        return [x for x in re.split('[,+]', s) if x]

    def to_url(self, values):
        return ','.join(x for x in values if x)
