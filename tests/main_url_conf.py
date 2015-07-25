from . import views
from urljects import U, I, url


urlpatterns = [
    url(U / 'test_view', views.test_view),
    url(U / 'class_view', views.ClassTestView),
]