from . import views
from .included_app import views as included_views
from urljects import U, url, view_include


urlpatterns = [
    url(U / 'test_view', views.test_view),

    url(U / 'included', view_include(included_views)),
    url(U / 'included', view_include(included_views, namespace='named'))
]
