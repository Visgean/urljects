import re

beginning = r'^'
end = r'$'

slug = r'(?P<slug>[\w-]+)'
pk = '(?P<pk>\d+)'
uuid4 = '(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'  # noqa
rest = '(?P<rest>[\w\-\_\.\@\:/]*)'  # match anything acceptable in URL

year = r'(?P<year>\d{4})'
month = r'(?P<month>0?([1-9])|10|11|12)'
day = r'(?P<day>(0|1|2)?([1-9])|[1-3]0|31)'

SEPARATOR = '/'  # separator for parts of the url

RE_TYPE = re._pattern_type   # pylint:disable=protected-access


def render(parts, separator=SEPARATOR, ends=True):
    """
    This function finishes the url pattern creation by adding starting
    character ^ end possibly by adding end character at the end

    :param parts: URL parts
    :param separator: used to separate parts of the url, usually /
    :param ends: open urls should be used only for included urls
    :return: raw string
    """
    value = separator.join(parts)

    if not value:  # use case: wild card imports
        if ends:
            return r'^$'
        return r'^'

    if value[0] != beginning:
        value = beginning + value

    if ends and value[-1] != end:
        value += end

    # included views usually ends with separator
    if not ends and value[-1] != separator:
        value += separator

    return value


class URLPattern(str):
    """The main urljects object able to join strings and regular expressions.

    The value of this object will always be regular expression usable in django
    url.
    """
    def __new__(cls, value='', separator=SEPARATOR, ends=True):
        """
        :param value: Initial value of the URL
        :param separator: used to separate parts of the url, usually /
        :param ends: open urls should be used only for included urls
        """
        parts = (value.strip(separator),) if value else ()
        self = str.__new__(cls, render(parts, separator, ends))
        self.parts = parts
        self.separator = separator
        self.ends = ends
        return self

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
            # stripping separator enables translated urls with hint what
            # string is actual url and which is a normal word
            # url(U / _('/my-profile'), private.Home, name="admin-home"),
            parts = self.parts + (part.strip(self.separator),)
            return URLPattern(
                value=self.separator.join(parts),
                separator=self.separator,
                ends=self.ends)
        return self

    def get_value(self, ends_override=None):
        ends = self.ends if ends_override is None else ends_override
        return render(self.parts, self.separator, ends)

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
        return self or ''


U = URLPattern()
