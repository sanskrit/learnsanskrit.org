# -*- coding: utf-8 -*-
"""
    lso.lib.converters
    ~~~~~~~~~~~~~~~~~~

    Routing converters

    :license: MIT and BSD
"""
from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):

    """Converter for list data"""

    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return ','.join(values)
