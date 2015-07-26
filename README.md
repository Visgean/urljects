Django URL Objects = URLjects
=============================

[![Travis CL](https://img.shields.io/travis/Visgean/urljects.svg)](https://travis-ci.org/Visgean/urljects)
[![Documentation Status](https://readthedocs.org/projects/urljects/badge/?version=latest)](https://urljects.readthedocs.org/en/latest/)
[![Pypi](https://img.shields.io/pypi/v/urljects.svg)](https://pypi.python.org/pypi/urljects)
[![Code Health](https://landscape.io/github/Visgean/urljects/master/landscape.svg?style=flat)](https://landscape.io/github/Visgean/urljects/master)
[![Join the chat at https://gitter.im/Visgean/urljects](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Visgean/urljects)



URLjects Patterns
-----------------

With URLjects you can write this

```python
from urljects import U, slug

url_patterns = (
    url(U / 'detail' / slug, view=DetailView),
)
```

instead of this:

```python 
url_patterns = (
    url(r'^detail/(?P<slug>[\w-]+)' , view=DetailView.as_view(), 
        name='detail'),
)
```

The name of the view has been taken from ``DetailView.url_name``.
There are also some common regular patterns like slugs and UUIDs so that you
can focus on more important stuff than on debugging regular expressions.


Routing without urls.py
-----------------------

With the use of ``include_view()`` you can avoid using included ``urls.py``
and include views directly. 

For class based views simply inherit from ``URLView``.

```python
class ItemDetail(URLView, DetailView):
    name = 'detail'
    url = U / 'detail' / slug
```

a lot of people enjoy functional views, for those there is ``url_view`` decorator.

```python
@url_view(U / 'detail' / slug)
def detail(request, slug)
    ...
```