Three ways of routing
=====================

Under URLjects there are three main ways of urls. You should stick to one and
avoid mixing them.


The way of file
---------------

This is pretty standard way of dealing with routing, you put your urls into
file called ``urls.py`` and register that file with django. Nice and tidy. ::

    from urljects import url, U, slug
    from views import main_view, ClassView

    urlpatterns = ('',
        url(U / 'main', main_view),
        url(U / slug / 'classy', ClassView)
    )


The way of decorator
--------------------

This technique is practiced for centuries by masters of Flask. This is only
useful if you are in the Function Based Views alliance.


Tha classy way
--------------

If you are with Class Based Views army you should go with this approach.