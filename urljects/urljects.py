import re
import patterns


class URLPattern(object):
    """
    This is the main urljects object, it is able to join strings and
    regular expressions. The value of this object will always be regular
    expression usable in django url.
    """

    def __init__(self, value=None, separator=patterns.SEPARATOR, ends=True):
        """
        :param value: Initial value of the URL
        :param separator: used to separate parts of the url, usually /
        :param ends: open urls should be used only for included urls
        """
        self.value = value
        self.separator = separator
        self.ends = ends

    def add_part(self, part):
        """
        Function for adding partial pattern to the value
        :param part: string or compiled pattern
        """
        if isinstance(part, re._pattern_type):
            part = part.pattern

        if self.value is None:
            # This enables the U / '' syntax
            return URLPattern(
                value=part,
                separator=self.separator,
                ends=self.ends)
        else:
            self.value += self.separator + part
        return self

    def get_value(self):
        """
        This function finishes the url pattern creation by adding starting
        character ^ end possibly by adding end character at the end
        :return: raw string
        """
        value = self.value
        if self.value[0] != patterns.beginning:
            value = patterns.beginning + self.value

        if self.ends and self.value[-1] != patterns.end:
            value += patterns.end
        return value

    def __div__(self, other):
        return self.add_part(other)

    def __repr__(self):
        return self.get_value() or ''


U = URLPattern()
I = URLPattern(ends=False)
