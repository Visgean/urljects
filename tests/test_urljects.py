# -*- coding: utf-8 -*-
from __future__ import absolute_import

import django
import mock
import os
import re
import unittest

from django.core.urlresolvers import reverse
from collections import namedtuple
from urljects import U, slug, url
from . import views

DJANGO_GTE_1_9 = django.VERSION[:2] >= (1, 9)

URLTest = namedtuple('URLTest', ['old_url', 'new_url'])
test_data = [
    URLTest(
        old_url=r'^detail/(?P<slug>[\w-]+)$',
        new_url=U / 'detail' / slug,
    ),
    URLTest(
        old_url=r'^(?P<slug>[\w-]+)$',
        new_url=U / slug,
    ),
    URLTest(
        old_url=r'^static$',
        new_url=U / 'static',
    ),
]


class TestURLjects(unittest.TestCase):
    def test_regulars(self):
        """Test that old_url is same as new_url."""
        for url_test in test_data:
            self.assertEqual(url_test.old_url, url_test.new_url)

    def test_str_method(self):
        """Test that stringification returns expected value."""
        for url_test in test_data:
            self.assertEqual(
                str(url_test.new_url),
                url_test.new_url)

    def test_compile(self):
        """Tests that U object can actually compile to regex."""
        patterns_to_compile = (g.new_url for g in test_data)
        for pattern in patterns_to_compile:
            re.compile(pattern)

    def test_compiled_pattern(self):
        """Tests that U object can work with compiled patterns."""
        compiled_slug = re.compile(slug)
        self.assertEqual(
            (U / 'something' / compiled_slug),
            (U / 'something' / slug))

    def test_separated_values(self):
        """Tests that separator in values does not lead to double-separated url."""
        self.assertEqual(
            (U / '/something'),
            '^/something$')
        self.assertEqual(
            (U / 'something' / '/else'),
            (U / 'something' / 'else'))
        self.assertEqual(
            (U / '/something' / '/else'),
            '^/something/else$')


class TestURL(unittest.TestCase):
    """
    Tests urljects.url function, basically this only tests that django internal
    url function is being called correctly and since it is extensively tested
    by django internal tests we can already assume that it is working if it is
    being called correctly
    """

    @mock.patch('django.conf.urls.url')
    def test_func_view(self, mocked_url):
        url(U, view=views.test_view)
        mocked_url.assert_called_once_with(
            regex='^$',
            view=views.test_view,
            kwargs=None,
            name='test_view',
        )

    @unittest.skipIf(DJANGO_GTE_1_9, "Django >= 1.9 has deprecated string views")
    @mock.patch('django.conf.urls.url')
    def test_string_view(self, mocked_url):
        url(U / 'test', view='views.test_view')
        mocked_url.assert_called_once_with(
            regex='^test$',
            view='views.test_view',
            kwargs=None,
            name='test_view',
        )

    @mock.patch('django.conf.urls.url')
    def test_class_view(self, mocked_url):
        url(U / 'class_view', view=views.ViewClass)
        mocked_url.assert_called_once_with(
            regex='^class_view$',
            view=views.ViewClass.as_view(),
            kwargs=None,
            name=views.ViewClass.url_name,
        )


class TestAPP(unittest.TestCase):
    """Tests Django integration without mocking.

    URLs are registered in ``main_url_conf.py``
    """

    def setUp(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    def test_function_view(self):
        self.assertEqual(reverse(viewname='test_view'), u'/test_view')

    def test_included_views(self):
        self.assertEqual(reverse(viewname='included_view'),
                         u'/included/included_view')
        self.assertEqual(reverse(viewname='IncludedView'),
                         u'/included/IncludedView')

    def test_named_included_views(self):
        self.assertEqual(reverse(viewname='named:included_view'),
                         u'/included/included_view')
        self.assertEqual(reverse(viewname='named:IncludedView'),
                         u'/included/IncludedView')

    @unittest.skipIf(DJANGO_GTE_1_9, "Django >= 1.9 has deprecated string views")
    def test_string_included_views(self):
        self.assertEqual(reverse(viewname='string_import:included_view'),
                         u'/string/included_view')
        self.assertEqual(reverse(viewname='string_import:IncludedView'),
                         u'/string/IncludedView')

    @unittest.skipIf(DJANGO_GTE_1_9, "Django >= 1.9 has deprecated string views")
    def test_wild_card(self):
        self.assertEqual(reverse(viewname='wild_card:included_view'),
                         u'/included_view')
        self.assertEqual(reverse(viewname='wild_card:IncludedView'),
                         u'/IncludedView')

    def test_named_routed_views(self):
        self.assertEqual(reverse(viewname='routed:RoutedView'),
                         u'/routed/RoutedView')
        self.assertEqual(reverse(viewname='routed:routed_view'),
                         u'/routed/routed_view')
        self.assertEqual(reverse(viewname='routed:aliased_view'),
                         u'/routed/aliased_view')
        if not DJANGO_GTE_1_9:
            self.assertEqual(reverse(viewname='routed:string_view'),
                             u'/routed/string_view')
