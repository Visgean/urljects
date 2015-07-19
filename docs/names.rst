View name handling
------------------

If you don't specify name to ``urljects.url`` it will be derived automatically.

Functional views
----------------
::

    url(U, view=views.test_view)

here ``view.func_name`` will be used.

String views
------------
::

    url(U / 'test', view='views.test_view')

the last part of the string will be used.

Class Views
-----------

::

    url(U / 'class_view', view=views.ClassTestView)

``ClassTestView.name`` will be used.


