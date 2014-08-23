import unittest

from depparse import _sparse


class SparseTest(unittest.TestCase):
    def test_dot(self):
        fws = dict((str(i), float(i)) for i in xrange(100))
        self.assertEqual(10, _sparse.dot(fws, '1 2 3 4'.split()))
        self.assertEqual(14, _sparse.dot(fws, '2 3 4 5'.split()))

    def test_update(self):
        target = dict((str(i), float(i)) for i in xrange(10))
        source = dict((str(i), float(i)) for i in xrange(20))

        _sparse.update(target, source, 3)

        self.assertEqual(target, dict((str(i), i * (i >= 10 and 3 or 4))
                                      for i in xrange(20)))
