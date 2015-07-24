import re
import six
import inspect
import functools

from django.conf import urls
from . import patterns


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
I = URLPattern(ends=False)


class URLView(object):
    """
        Abstract class with url and name.

        Since URLs can't be changed on runtime it is kind of pointless
        to have ``get_url`` or ``get_url_name`` methods. So there are not any.
    """

    url = NotImplemented
    url_name = NotImplemented


def url_view(url_pattern, name=None):
    """
    Decorator for registering functional views.
    Meta decorator syntax has to be used in order to accept arguments.

    This decorator does not really do anything that magical, you could achieve

    This:
    >>> @url_view(U / 'my_view')
    ... def my_view(request)
    ...     pass

    is equivalent to this:
    >>> def my_view(request)
    ...     pass
    >>> my_view.urljects_view = True
    >>> my_view.url = U / 'my_view'
    >>> my_view.url_name = 'my_view'

    Those view are then supposed to be used with ``view_include`` which will
    register all views that have ``urljects_view`` set to ``True``.

    :param url_pattern: regex or URLPattern or anything passable to url()
    :param name: name of the view, func_name will be used otherwise.
    """

    def meta_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.urljects_view = True
        wrapper.url = url_pattern
        wrapper.url_name = name or func.func_name

        return wrapper
    return meta_wrapper


def resolve_name(view):
    """
    Auto guesses name of the view.
    For function it will be ``view.func_name``
    For classes it will be ``view.url_name``
    """
    if hasattr(view, 'func_name'):
        return view.func_name
    if hasattr(view, 'url_name'):
        return view.url_name
    if isinstance(view, six.string_types):
        return view.split('.')[-1]
    return None


def url(regex, view, kwargs=None, name=None, prefix=''):
    """
    This is replacement for ``django.conf.urls.url`` function.
    This url auto calls ``as_view`` method for Class based views and resolves
    URLPattern objects.

    If ``name`` is not specified it will try to guess it.

    :param regex: string with regular expression or URLPattern
    :type regex: URLPattern
    :param view: function/string/class of the view
    :param kwargs: kwargs that are to be passed to view
    :param name: name of the view, if empty it will be guessed
    :param prefix: useless, use namespaces
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


def view_include(view_module, namespace=None, app_name=None):
    """
    Includes view in the url, works similar to django include function.
    Auto imports all class based views that are subclass of ``URLView`` and
    all functional views that have been decorated with ``url_view``.

    :param view_module: object of the module or string with importable path
    :param namespace: name of the namespaces, it will be guessed otherwise
    :param app_name: application name
    :return: result of url include
    """

    # since Django 1.8 patterns() are deprecated, list should be used instead
    view_patterns = []

    if isinstance(view_module, six.string_types):
        view_module = __import__(view_module)

    for member in inspect.getmembers(view_module):
        is_class_view = inspect.isclass(member) and issubclass(member, URLView)
        is_func_view = (inspect.isfunction(member)
                        and hasattr(member, 'urljects_view')
                        and member.urljects_view)
        if is_class_view or is_func_view:
            view_patterns.append(url(member.url, member, name=member.url_name))

    return urls.include(
        arg=view_patterns,
        namespace=namespace,
        app_name=app_name)
