===============================
Django URL Objects - urljects
===============================

.. image:: https://img.shields.io/travis/Visgean/urljects.svg
        :target: https://travis-ci.org/Visgean/urljects

.. image:: https://img.shields.io/pypi/v/urljects.svg
        :target: https://pypi.python.org/pypi/urljects         

Django URLS rethinked

* Free software: BSD license
* Documentation: https://urljects.readthedocs.org.

So, about a year ago I was thinking about this genial idea: I have seen a lot of python code dealing with paths. Lot of os.path.join methods... Well if you have worked with files in python you get the picture. So I had this idea: what if you could just type something like:

```
path = P / 'tmp' / 'file'
```
and everything would be resolved magically. Well after couple of minutes of Googling I discovered [pathlib](https://docs.python.org/3/library/pathlib.html). This module is really brilliant. So it set me thinking: what else could be represented in this fashion: URLS! 

Ugliness of Django routing system
------------------------------------------------------

Adding new views in Django is done usually in two files: in ``views.py`` where most of the stuff go and then it is registered in ``urls.py``. 

This sucks, especcially if you are using Class-Based-Views: 

```
url(r'^add$', views.AddSource.as_view(), name='add'),
```

I hate calling ``as_view`` method in ``urls.py```, this could have been resolved automatically!

Another reason why writing urls causes me pain is because of Regular expressions. Yes they useful, they are nice. But they should not be ever-present  as they are in Django where you can't write a single url without it. But even worst they are error-prone. 
In reality there is not so many things people try to parse in Django urls:

 - Slugs ``(?P<slug>[\w-]+)``
 - IDs ``(?P<pk>\d+)``
 - static strings ``(?P<section>body|footer)``
 - UUIDs ``(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})``

These are common patterns and as you can see they are hard to remember and error prone. If you look at the StackOveflow you will find a lot of questions about this. 

Idea
------

I would like to use something like this:

```
from urljects import U, slug, pk

url_patterns = (
    url(U / 'detail' / slug, view=DetailView, name='detail'),
)
```

This code should be equivalent to this:
```python 

url_patterns = (
    url(r'^detail/(?P<slug>[\w-]+)' , view=DetailView.as_view(), 
        name='detail'),
)
```

URLs without explicit registration
============================

Class based views
----------------------------

The Django way of routing is to link views with regular expressions in silly files named ``urls.py``. It is silly cause every time you change/add/remove view you also have to change it in another file. 

One thing that I like about Django are models. You create file named ``models.py`` add some models and you are good to go. No registration. 

There is no reason why this should not work the same way with views:

```

class ItemDetail(URLview, DetailView):
       name = 'detail'
       url = U / 'detail' / slug
```

Decorator based registration
--------------------------------------------
A lot of people enjoy decorator based urls:

```

@url(U / 'detail' / slug)
def detail(request, slug)
     ...

```

Naming and namespace
--------------------------------------

View names and namespaces should be automatically resolved. 
Namespace should be derived from app label and view name should be derived form function / class name. 

