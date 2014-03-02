# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

from gibi import Matrix
from gibi.io import FrenchNormalizer
from gibi.matrix import bigrams, feed_matrix
from six import StringIO


class TestMatrix(object):
    @staticmethod
    def test_inexistant_transition():
        m = Matrix()
        assert m.transition('a', 'b') == 0

    @staticmethod
    def test_one_edge():
        m = Matrix()
        m.increment('a', 'b')
        assert m.transition('a', 'b') == 1

    @staticmethod
    def test_two_edges():
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transition('a', 'b') == 0.5

    @staticmethod
    def test_three_edges():
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transition('a', 'b') == 2 / 3

    @staticmethod
    def test_transitions():
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transitions('a') == {
            'b': (2 / 3),
            'c': (1 / 3),
        }


class TestBigrams(object):
    @staticmethod
    def on_zero():
        assert list(bigrams([])) == []

    @staticmethod
    def on_one():
        assert list(bigrams([1])) == []

    @staticmethod
    def on_two():
        assert list(bigrams([1, 2])) == [(1, 2)]

    @staticmethod
    def on_three():
        assert list(bigrams([1, 2, 3])) == [(1, 2), (2, 3)]

    @staticmethod
    def on_four():
        assert list(bigrams([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]


# noinspection PyAttributeOutsideInit
class TestMatrixFeeding(object):
    def setup_class(self):
        self.m = Matrix()

    def feed_simple(self):
        r = StringIO('ab')
        n = FrenchNormalizer(r)

        feed_matrix(n, self.m)

        assert self.m.transition('a', 'b') == 1

    def feed_less_simple(self):
        r = StringIO('ababac')
        n = FrenchNormalizer(r)

        feed_matrix(n, self.m)

        assert self.m.transitions('a') == {
            'b': (2 / 3),
            'c': (1 / 3),
        }
