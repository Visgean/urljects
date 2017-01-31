import django
from django.views.generic.base import View

from urljects import RouteMap, U

DJANGO_GTE_1_9 = django.VERSION[:2] >= (1, 9)

route = RouteMap()


@route(U / 'RoutedView', name='RoutedView')
class RoutedView(View):
    pass


@route(U / 'routed_view')
@route(U / 'aliased_view', name='aliased_view')
def routed_view():
    pass


def string_view():
    pass

if not DJANGO_GTE_1_9:
    route(U / 'string_view', 'tests.included_app.routed_views.string_view')
