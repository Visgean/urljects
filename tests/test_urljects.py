#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest
import mock
import views

from collections import namedtuple
from urljects import I, U, slug, url


URLTest = namedtuple('URLTest', ['old_url', 'new_url', 'view', 'name'])
test_data = [
    URLTest(
        old_url=r'^detail/(?P<slug>[\w-]+)$',
        new_url=U / 'detail' / slug,
        view=None,
        name=None
    ),
    URLTest(
        old_url=r'^(?P<slug>[\w-]+)$',
        new_url=U / slug,
        view=None,
        name=None
    ),
    URLTest(
        old_url=r'^static$',
        new_url=U / 'static',
        view=None,
        name=None
            ),
    URLTest(
        old_url=r'^products',
        new_url=I / 'products',
        view=None,
        name=None
    ),
]


class TestURLjects(unittest.TestCase):
    def test_regulars(self):
        """
        Test that old_url is same as new_url
        """
        for url_test in test_data:
            self.assertEqual(url_test.old_url, url_test.new_url.get_value())

    def test_compile(self):
        """
        Tests that U object can actually compile to regex
        """
        patterns_to_compile = (g.new_url for g in test_data)
        for pattern in patterns_to_compile:
            re.compile(pattern.get_value())


class TestURL(unittest.TestCase):
    """
    Tests urljects.url function, basically this only tests that django internal
    url function is being called correctly and since it is extensively tested
    by django internal tests we can already assume that it is working if it is
    being called correctly
    """

    @mock.patch('django.conf.urls.url')
    def test_func_view(self, mocked_url):
        url(U, view=views.test_view, prefix='prefix')
        mocked_url.assert_called_once_with(
            regex='^$',
            view=views.test_view,
            kwargs=None,
            name='test_view',
            prefix='prefix'
        )

    @mock.patch('django.conf.urls.url')
    def test_string_view(self, mocked_url):
        url(U / 'test', view='views.test_view')
        mocked_url.assert_called_once_with(
            regex='^test$',
            view='views.test_view',
            kwargs=None,
            name='test_view',
            prefix=''
        )

    @mock.patch('django.conf.urls.url')
    def test_class_view(self, mocked_url):
        url(U / 'class_view', view=views.ClassTestView)
        mocked_url.assert_called_once_with(
            regex='^class_view$',
            view=views.ClassTestView.as_view(),
            kwargs=None,
            name=views.ClassTestView.name,
            prefix=''
        )
