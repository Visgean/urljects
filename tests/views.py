from django.views.generic.base import View

def test_view():
    pass


class ClassTestView(View):
    url_name = 'class_test_view'
