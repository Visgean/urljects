import re

beginning = r'^'
end = r'$'

slug = r'(?P<slug>[\w-]+)'
pk = '(?P<pk>\d+)'
uuid4 = '(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'  # noqa

year = r'(?P<year>\d{4})'
month = r'(?P<month>0?([1-9])|10|11|12)'
day = r'(?P<day>(0|1|2)?([1-9])|[1-3]0|31)'

SEPARATOR = '/'  # separator for parts of the url

RE_TYPE = re._pattern_type   # pylint:disable=protected-access


class URLPattern(object):
    """
    This is the main urljects object, it is able to join strings and
    regular expressions. The value of this object will always be regular
    expression usable in django url.
    """

    def __init__(self, value=None, separator=SEPARATOR, ends=True):
        """
        :param value: Initial value of the URL
        :param separator: used to separate parts of the url, usually /
        :param ends: open urls should be used only for included urls
        """
        self.parts = [value] if value else []
        self.separator = separator
        self.ends = ends

    def add_part(self, part):
        """
        Function for adding partial pattern to the value
        :param part: string or compiled pattern
        """
        if isinstance(part, RE_TYPE):
            part = part.pattern

        if not self.parts:
            # This enables the U / '' syntax
            return URLPattern(
                value=part,
                separator=self.separator,
                ends=self.ends)
        else:
            self.parts.append(part)
        return self

    def get_value(self, ends_override=None):
        """
        This function finishes the url pattern creation by adding starting
        character ^ end possibly by adding end character at the end

        :param ends_override: overrides ``self.ends``
        :return: raw string
        """
        value = self.separator.join(self.parts)
        ends = ends_override if ends_override is not None else self.ends

        if not value:  # use case: wild card imports
            if ends:
                return r'^$'
            return r'^'

        if value[0] != beginning:
            value = beginning + value

        if ends and value[-1] != end:
            value += end

        # included views usually ends with separator
        if not ends and value[-1] != self.separator:
            value += self.separator

        return value

    def __div__(self, other):
        """
        PY2 division
        """
        return self.add_part(other)

    def __truediv__(self, other):
        """
        PY3 division
        """
        return self.add_part(other)

    def __repr__(self):
        return self.get_value() or ''


U = URLPattern()
