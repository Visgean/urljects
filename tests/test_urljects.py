#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from urljects import U, slug


class TestUrljects(unittest.TestCase):
    def test_regulars(self):
        test_data = [
            [
                r'^detail/(?P<slug>[\w-]+)',
                U / 'detail' / slug
            ]
        ]

        for old, new in test_data:
            print new
            self.assertEqual(old, new.value)


if __name__ == '__main__':
    unittest.main()
