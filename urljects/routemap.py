import operator

from django.conf import urls

from .urljects import url, resolve_name


class RouteMap(object):
    """
        Records mapping of URLs to views
    """

    def __init__(self):
        self.routes = []

    def __call__(self, url_pattern, view=None, name=None, priority=0,
                 kwargs=None):
        """
        Register a URL -> view mapping, or return a registering decorator

        :param url_pattern: regex or URLPattern or anything passable to url()
        :param view: The view. If None, a decorator will be returned

        The remaining arguments should be given by name:

        :param name: name of the view; resolve_name() will be used otherwise.
        :param priority: priority for sorting; pass e.g. -1 for catch-all route
        """

        def router_decorator(view):
            if name is None:
                resolved_name = resolve_name(view)
            else:
                resolved_name = name
            url_object = url(url_pattern, view, kwargs=kwargs,
                             name=resolved_name)
            self.routes.append((priority, url_object))
            return view

        # If view was given, decorate it immediately
        if view is not None:
            return router_decorator(view)

        return router_decorator

    def include(self, location, namespace=None, app_name=None):
        """
        Return an object suitable for url_patterns.

        :param location: root URL for all URLs from this router
        :param namespace: passed to url()
        :param app_name: passed to url()
        """
        sorted_entries = sorted(self.routes, key=operator.itemgetter(0),
                                reverse=True)

        # pylint:disable=unused-variable
        arg = [u for p, u in sorted_entries]
        return url(location, urls.include(
            arg=arg,
            namespace=namespace,
            app_name=app_name))
