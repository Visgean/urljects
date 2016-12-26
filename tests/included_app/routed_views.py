from django.views.generic.base import View

from urljects import RouteMap, U

route = RouteMap()


@route(U / 'RoutedView', name='RoutedView')
class RoutedView(View):
    pass


@route(U / 'routed_view')
@route(U / 'aliased_view', name='aliased_view')
def routed_view():
    pass
