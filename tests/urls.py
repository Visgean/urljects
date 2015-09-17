from . import views
from .included_app import views as included_views
from .included_app.routed_views import route as routed_views
from urljects import U, url, view_include


urlpatterns = [
    url(U / 'test_view', views.test_view),

    url(U / 'included', view_include(included_views)),
    url(U / 'included', view_include(included_views, namespace='named')),
    url(U / 'string', view_include('tests.included_app.views',
                                   namespace='string_import')),
    url(U, view_include(included_views, namespace='wild_card')),
    routed_views.include(U / 'routed', namespace='routed'),
]
