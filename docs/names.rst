View name handling
==================

If you don't specify name to ``urljects.url`` it will be derived automatically.

Functional views
----------------
::

    url(U, view=views.test_view)

here ``view.__name__`` will be used.

String views
------------
::

    url(U / 'test', view='views.test_view')

the last part of the string will be used.

Class Views
-----------

::

    url(U / 'class_view', view=views.ClassTestView)

``ClassTestView.url_name`` will be used.


Namespace
---------

So far there is no support for auto-guessing namespaces based on app. 