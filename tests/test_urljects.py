#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest

from urljects import U, slug


class TestUrljects(unittest.TestCase):
    test_data = [
        [
            r'^detail/(?P<slug>[\w-]+)$',
            U / 'detail' / slug
        ],
    ]

    def test_regulars(self):
        for old, new in self.test_data:
            self.assertEqual(old, new.get_value())

    # def test_compile(self):
    #     """
    #     Tests that U object can actually compile to regex
    #     """
    #
    #     re.compile(U / 'detail' / slug)


if __name__ == '__main__':
    unittest.main()
