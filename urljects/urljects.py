import six
import inspect
import functools
import importlib

from collections import defaultdict
from django.conf import urls
from .patterns import URLPattern


class URLView(object):
    """
        Abstract class with url and name.

        Since URLs can't be changed on runtime it is kind of pointless
        to have ``get_url`` or ``get_url_name`` methods. So there are not any.
    """

    url = NotImplemented
    url_name = NotImplemented
    url_priority = None


def url_view(url_pattern, name=None, priority=None):
    """
    Decorator for registering functional views.
    Meta decorator syntax has to be used in order to accept arguments.

    This decorator does not really do anything that magical:

    This:
    >>> from urljects import U, url_view
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
    :param name: name of the view, __name__ will be used otherwise.
    :param priority: priority of the view, the lower the better
    """

    def meta_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.urljects_view = True
        wrapper.url = url_pattern
        wrapper.url_name = name or func.__name__
        wrapper.url_priority = priority

        return wrapper
    return meta_wrapper


def resolve_name(view):
    """
    Auto guesses name of the view.
    For function it will be ``view.__name__``
    For classes it will be ``view.url_name``
    """
    if inspect.isfunction(view):
        return view.__name__
    if hasattr(view, 'url_name'):
        return view.url_name
    if isinstance(view, six.string_types):
        return view.split('.')[-1]
    return None


def url(url_pattern, view, kwargs=None, name=None):
    """
    This is replacement for ``django.conf.urls.url`` function.
    This url auto calls ``as_view`` method for Class based views and resolves
    URLPattern objects.

    If ``name`` is not specified it will try to guess it.

    :param url_pattern: string with regular expression or URLPattern
    :param view: function/string/class of the view
    :param kwargs: kwargs that are to be passed to view
    :param name: name of the view, if empty it will be guessed
    :param prefix: useless, use namespaces
    """
    if isinstance(url_pattern, URLPattern):
        if isinstance(view, tuple):  # this is included view
            url_pattern = url_pattern.get_value(ends_override=False)
        else:
            url_pattern = url_pattern.get_value()

    if name is None:
        name = resolve_name(view)

    if callable(view) and hasattr(view, 'as_view') and callable(view.as_view):
        view = view.as_view()

    return urls.url(
        regex=url_pattern,
        view=view,
        kwargs=kwargs,
        name=name,
        )


def view_include(view_module, namespace=None, app_name=None):
    """
    Includes view in the url, works similar to django include function.
    Auto imports all class based views that are subclass of ``URLView`` and
    all functional views that have been decorated with ``url_view``.

    :param view_module: object of the module or string with importable path
    :param namespace: name of the namespaces, it will be guessed otherwise
    :param app_name: application name
    :return: result of urls.include
    """

    # since Django 1.8 patterns() are deprecated, list should be used instead
    # {priority:[views,]}
    view_dict = defaultdict(list)

    if isinstance(view_module, six.string_types):
        view_module = importlib.import_module(view_module)

    # pylint:disable=unused-variable
    for member_name, member in inspect.getmembers(view_module):
        is_class_view = inspect.isclass(member) and issubclass(member, URLView)
        is_func_view = (inspect.isfunction(member) and
                        hasattr(member, 'urljects_view') and
                        member.urljects_view)

        if (is_class_view and member is not URLView) or is_func_view:
            view_dict[member.url_priority].append(
                url(member.url, member, name=member.url_name))

    view_patterns = list(*[
        view_dict[priority] for priority in sorted(view_dict)
        ])

    return urls.include(
        arg=view_patterns,
        namespace=namespace,
        app_name=app_name)
