

def test_view():
    pass


class ClassTestView(object):
    url_name = 'class_test_view'

    @staticmethod
    def as_view():
        return 'ClassTestView'
