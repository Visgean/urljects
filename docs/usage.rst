Using URLjects
==============

Under URLjects there are three main ways of urls. You should stick to one and
avoid mixing them.


Using in urls.py
----------------

This is pretty standard way of dealing with routing, you put your urls into
file called ``urls.py`` and register that file with django. Nice and tidy. ::

    from urljects import url, U, slug
    from views import main_view, ClassView

    urlpatterns = ('',
        url(U / 'main', main_view),
        url(U / slug / 'classy', ClassView)
    )


Note that you have to import ``urljects.url`` and not django version.


Using view_include
------------------

If you are tired of having so many ``urls.py`` files you can use ``view_include``
to directly import views to main urlconf. So your ``urlconf`` will look like this:

::

    urlpatterns = [
        url(U / 'eshop', view_include(eshop_views)),
        url(U / 'blog', view_include(blog_views, namespace='named'))
    ]

Note that views have to either decorated with ``url_view`` function or for class
based views they will have to inherit from ``URLView`` class.

Class based views:
::

    class DetailView(View, URLView):
        url = U / 'detail' / slug
        url_name = 'detail_view'
        url_priority = -1


Function based views:
::

    @url_view(U / 'detail' / slug, priority=-1)
    def detail_view(request):
        return render()

If you don't specify url name for functional views it will be derived from
function name.



Using the RouteMap
----------------

An alternative to ``URLView`` and ``@url_view`` is the RouteMap.

The RouteMap is an object that maps URLs to routes. Usually, one is created
in every view module, and named "route". With class and callable views,
it's used as a decorator::

    from urljects import RouteMap
    route = RouteMap()

    @route(U / 'post')
    def post_view():
        return render()

    @route(U / 'detail', name='detail_view')
    class DetailView(View):
        pass

It can also be used as a function, typically for view names as strings::

    route(U / 'profile', 'users_app.views.profile_view')

In urls.py, use the RouteMap's ``include`` method::

    from my_app.blog.views import route as blog_routemap
    urlpatterns = [
        blog_routemap.include(U / 'blog')
    ]

The ``@route`` decorator may be used multiple times on a single view.
The URLs it records are included in the order the views are defined in,
or they can be given a priority::

    @route(U / slug, priority=-1)
    def post_view():
        """ A catch-all view with low priority """
        return render()
