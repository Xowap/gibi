# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

from gibi import Matrix
from gibi.io import FrenchNormalizer
from gibi.matrix import bigrams
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
        assert m.transition('a', 'b') == 1

    @staticmethod
    def test_three_edges():
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transition('a', 'b') == 2

    @staticmethod
    def test_transitions():
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transitions('a') == {
            'b': 2,
            'c': 1,
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
    @staticmethod
    def test_feed_simple():
        r = StringIO('ab')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.transition('a', 'b') == 1

    @staticmethod
    def test_feed_less_simple():
        r = StringIO('ababac')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.transitions('a') == {
            'b': 2,
            'c': 1,
        }


# noinspection PyAttributeOutsideInit
class TestWordGeneration(object):
    @staticmethod
    def test_choose_simple_transition():
        trans = Matrix.choose_transition({
            'a': 0.4,
            'b': 0.6
        }, 0)

        assert trans == 'a'

        trans = Matrix.choose_transition({
            'a': 0.6,
            'b': 0.4
        }, 0)

        assert trans == 'b'

    @staticmethod
    def test_choose_transition():
        trans = Matrix.choose_transition({
            'a': 1,
            'b': 1,
            'c': 1,
            False: 1,
            True: 1,
        }, 0.5)

        assert trans == 'c'

    @staticmethod
    def test_generate_simple_word():
        r = StringIO('abc')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.make_word() == 'abc'

    @staticmethod
    def test_generate_word():
        r = StringIO('bonjour youpi tralala pouet youpla')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.make_word(10) == 'tr'

    @staticmethod
    def test_deterministic():
        r = StringIO('ab ac')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
        assert m.make_word(42) == m.make_word(42)
