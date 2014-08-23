import unittest
import collections

from depparse.perceptron import VotedPerceptron


class PerceptronTest(unittest.TestCase):
    def _vp(self):
        def weights(a=lambda: dict(y=2.0, z=3.0),
                    b=lambda: dict(x=3.0, y=2.0),
                    c=lambda: dict(x=5.0)):
            return dict(
                a=collections.defaultdict(int, a()),
                b=collections.defaultdict(int, b()),
                c=collections.defaultdict(int, c()))

        vp = VotedPerceptron(20)

        vp._acc_weights = weights()
        vp._acc_iterations = collections.defaultdict(
            float, dict(a=5.0, b=3.0, c=1.0))

        vp._cur_weights = weights(a=lambda: dict(w=2.0, y=3.0, z=3.0))
        vp._cur_iterations = collections.defaultdict(
            float, dict(a=3.0, b=1.0, c=0.0))

        return vp

    def assertWeights(self, **weights):
        self.assertEqual(set(weights), set(self.vp._acc_weights))
        for label, expected in weights.items():
            actual = self.vp._acc_weights.get(label)
            self.assert_(actual is not None)
            self.assertEqual(expected, actual,
                '%s: expected %r, got %r' % (label, expected, actual))

    def setUp(self):
        self.vp = self._vp()

    def test_accumulate(self):
        self.vp._accumulate('a')
        self.assertWeights(a=dict(w=6, y=11, z=12),
                           b=dict(x=3, y=2),
                           c=dict(x=5))
        self.assertEqual(dict(a=0, b=1, c=0), self.vp._cur_iterations)
        self.vp._accumulate('b')
        self.assertWeights(a=dict(w=6, y=11, z=12),
                           b=dict(x=6, y=4),
                           c=dict(x=5))
        self.assertEqual(dict(a=0, b=0, c=0), self.vp._cur_iterations)
        self.vp._accumulate('c')
        self.assertWeights(a=dict(w=6, y=11, z=12),
                           b=dict(x=6, y=4),
                           c=dict(x=5))
        self.assertEqual(dict(a=0, b=0, c=0), self.vp._cur_iterations)

    def test___iadd__(self):
        other = self._vp()
        self.vp += other
        self.assertEqual(set(self.vp._acc_weights), set(other._acc_weights))
        self.assertWeights(a=dict(w=6, y=13, z=15),
                           b=dict(x=9, y=6),
                           c=dict(x=10))

    def test_train_correct(self):
        self.vp.train(tuple('y z'.split()), 'a')
        self.assertEqual(dict(a=4, b=1, c=0), self.vp._cur_iterations)
        self.assertEqual(dict(a=6.0, b=3.0, c=1.0), self.vp._acc_iterations)
        self.assertWeights(a=dict(y=2, z=3),
                           b=dict(x=3, y=2),
                           c=dict(x=5))

    def test_train_incorrect_existing(self):
        self.assertEqual(dict(a=3, b=1, c=0), self.vp._cur_iterations)
        self.assertEqual(dict(a=5.0, b=3.0, c=1.0), self.vp._acc_iterations)
        self.assertWeights(a=dict(y=2, z=3),
                           b=dict(x=3, y=2),
                           c=dict(x=5))

        self.vp.train(tuple('y z'.split()), 'c')
        self.assertEqual(dict(a=0, b=1, c=0), self.vp._cur_iterations)
        self.assertEqual(dict(a=5.0, b=3.0, c=2.0), self.vp._acc_iterations)
        self.assertWeights(a=dict(w=6, y=11, z=12),
                           b=dict(x=3, y=2),
                           c=dict(x=5))

        self.vp.train(tuple('y z'.split()), 'c')
        self.assertEqual(dict(a=0, b=1, c=0), self.vp._cur_iterations)
        self.assertEqual(dict(a=5.0, b=3.0, c=3.0), self.vp._acc_iterations)
        self.assertWeights(a=dict(w=6, y=11, z=12),
                           b=dict(x=3, y=2),
                           c=dict(x=5))
