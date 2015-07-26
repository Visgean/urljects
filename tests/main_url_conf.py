from . import views
from .included_app import views as included_views
from urljects import U, I, url, view_include


urlpatterns = [
    url(U / 'test_view', views.test_view),

    url(I / 'included', view_include(included_views)),
    url(I / 'included', view_include(included_views, namespace='named'))
]
