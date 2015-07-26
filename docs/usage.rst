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
        url_name = 'detail_view'
        url = U / 'detail' / slug


Function based views:
::

    @url_view(U / 'detail' / slug)
    def detail_view(request):
        return render()

If you don't specify url name for functional views it will be derived from
function name.