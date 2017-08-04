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


def render(value):
    """
    This function finishes the url pattern creation by adding starting
    character ^ end possibly by adding end character at the end

    :param value: naive URL value
    :return: raw string
    """
    # Empty urls
    if not value:  # use case: wild card imports
        return r'^$'

    if value[0] != beginning:
        value = beginning + value

    if value[-1] != end:
        value += end

    return value


class URLPattern(str):
    """The main urljects object able to join strings and regular expressions.

    The value of this object will always be regular expression usable in django
    url.
    """
    def __new__(cls, value='', separator=SEPARATOR):
        """
        :param value: Initial value of the URL
        :param separator: used to separate parts of the url, usually /
        """
        self = str.__new__(cls, render(value))
        self.separator = separator
        return self

    def add_part(self, part):
        """
        Function for adding partial pattern to the value
        :param part: string or compiled pattern
        """
        if isinstance(part, RE_TYPE):
            part = part.pattern

        # Allow U / spmething syntax
        if self == '^$':
            return URLPattern(part, self.separator)
        else:
            # Erase dup separator inbetween
            sep = self.separator
            return URLPattern(self.rstrip('$' + sep) + sep + part.lstrip(sep),
                              sep)

    # Python 2 and 3 division
    __div__ = __truediv__ = add_part

    def for_include(self):
        return self.rstrip('$' + self.separator) + self.separator


U = URLPattern()
