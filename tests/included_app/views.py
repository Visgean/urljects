from django.views.generic.base import View

from urljects import URLView, url_view, U


class IncludedView(View, URLView):
    url_name = 'IncludedView'
    url = U / 'IncludedView'


@url_view(U / 'included_view')
def included_view():
    pass
