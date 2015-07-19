Django URL Objects = urljects
=============================


[![Travis CL](https://img.shields.io/travis/Visgean/urljects.svg)](https://travis-ci.org/Visgean/urljects)
[![Documentation Status](https://readthedocs.org/projects/urljects/badge/?version=latest)](https://urljects.readthedocs.org/en/latest/)
[![Pypi](https://img.shields.io/pypi/v/urljects.svg)](https://pypi.python.org/pypi/urljects)
[![Code Health](https://landscape.io/github/Visgean/urljects/master/landscape.svg?style=flat)](https://landscape.io/github/Visgean/urljects/master)


Ugliness of Django routing system
---------------------------------

Adding new views in Django is done usually in two files: in ``views.py`` where most of the stuff go and then it is registered in ``urls.py``. 

This sucks, especcially if you are using Class-Based-Views: 

```
url(r'^add$', views.AddSource.as_view(), name='add'),
```

I hate calling ``as_view`` method in ``urls.py``, this should be resolved automatically!

Another things that sucks in Django URLs is Regular expressions. Yes they useful, they are nice. But they should not be ever-present,  you can't even write a single url without it. 
In reality there is not so many things people try to parse in Django urls:

 - Slugs ``(?P<slug>[\w-]+)``
 - IDs ``(?P<pk>\d+)``
 - static strings ``(?P<section>body|footer)``
 - UUIDs ``(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})``

These are common patterns and as you can see they are hard to remember and error prone.

The way of URLjects
-------------------

In URLjects you can write this

```python
from urljects import U, slug

url_patterns = (
    url(U / 'detail' / slug, view=DetailView),
)
```

which is equivalent to this:

```python 
url_patterns = (
    url(r'^detail/(?P<slug>[\w-]+)' , view=DetailView.as_view(), 
        name='detail'),
)
```

The name of view has been taken from ``DetailView.name``.

URLs without explicit registration
============================

Class based views
----------------------------

The Django way of routing is to link views with regular expressions in silly files named ``urls.py``. It is silly cause every time you change/add/remove view you also have to change it in another file. 

One thing that I like about Django are models. You create file named ``models.py`` add some models and you are good to go. No registration. 

There is no reason why this should not work the same way with views:

```python
class ItemDetail(URLview, DetailView):
       name = 'detail'
       url = U / 'detail' / slug
```

Decorator based registration
--------------------------------------------
A lot of people enjoy decorator based urls:


```python
@url(U / 'detail' / slug)
def detail(request, slug)
     ...
```

Naming and namespace
--------------------------------------

View names and namespaces should be automatically resolved. 
Namespace should be derived from app label and view name should be derived form function / class name. 

