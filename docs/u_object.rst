U object
========


``U`` object is ``URLPattern`` instance. It is used as replacement over regular
expression. It is similar to  .. _Pathlib.Path: https://docs.python.org/3/library/pathlib.html

You should combine U object with RE patterns, you can do it like this:

::

    from urljects import U, slug, url, view_include

    choice = r'(?P<choice>YES|NO)')

    urlpatterns = [
        url(U / 'detail' / slug, views.DetailView),   # -> r'^detail/(?P<slug>[\w-]+)$'
        url(U / choice, views.ChoiceView)             # -> r'^(?P<choice>YES|NO)')'

        url(U / 'eshop', view_include(eshop_views))   # -> r'^eshop/' + included urls
    ]

