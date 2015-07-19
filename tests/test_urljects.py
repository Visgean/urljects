#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

import re
import unittest

from urljects import I, U, slug


URLTest = namedtuple('URLTest', ['old_url', 'new_url', 'view', 'name'])


class TestURLjects(unittest.TestCase):
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

    def test_regulars(self):
        for url_test in self.test_data:
            self.assertEqual(url_test.old_url, url_test.new_url.get_value())

    def test_compile(self):
        """
        Tests that U object can actually compile to regex
        """
        patterns_to_compile = (g.new_url for g in self.test_data)
        for pattern in patterns_to_compile:
            re.compile(pattern.get_value())

if __name__ == '__main__':
    unittest.main()
