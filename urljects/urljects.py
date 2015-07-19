import re
import patterns

from django.conf import urls


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
        if value is None:
            value = patterns.beginning

        if value[0] != patterns.beginning:
            value = patterns.beginning + value

        if self.ends and value[-1] != patterns.end:
            value += patterns.end
        return value

    def __div__(self, other):
        return self.add_part(other)

    def __repr__(self):
        return self.get_value() or ''


U = URLPattern()
I = URLPattern(ends=False)


def resolve_name(view):
    """
    Auto guesses name of the view.
    For function it will be ``view.func_name``
    For classes it will be ``view.name``
    """
    if hasattr(view, 'func_name'):
        return view.func_name
    if hasattr(view, 'name'):
        return view.name
    if isinstance(view, basestring):
        return view.split('.')[-1]
    return None


def url(regex, view, kwargs=None, name=None, prefix=''):
    """
    This is replacement for ``django.conf.urls.url`` function.
    This url auto calls ``as_view`` method for Class based views and resolves
    URLPattern objects.

    If ``name`` is not specified it will try to guess it.
    """
    if isinstance(regex, URLPattern):
        regex = regex.get_value()

    if name is None:
        name = resolve_name(view)

    if callable(view) and hasattr(view, 'as_view') and callable(view.as_view):
        view = view.as_view()

    return urls.url(
        regex=regex,
        view=view,
        kwargs=kwargs,
        name=name,
        prefix=prefix)
