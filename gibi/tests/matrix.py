# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

from gibi import Matrix
from gibi.io import FrenchNormalizer
from gibi.matrix import tailgrams
from six import StringIO


# noinspection PyMethodMayBeStatic
class TestMatrix(object):
    def test_inexistant_transition(self):
        m = Matrix()
        assert m.transition('a', 'b') == 0

    def test_one_edge(self):
        m = Matrix()
        m.increment('a', 'b')
        assert m.transition('a', 'b') == 1

    def test_two_edges(self):
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transition('a', 'b') == 1

    def test_three_edges(self):
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transition('a', 'b') == 2

    def test_transitions(self):
        m = Matrix()
        m.increment('a', 'b')
        m.increment('a', 'b')
        m.increment('a', 'c')
        assert m.transitions('a') == {
            'b': 2,
            'c': 1,
        }


# noinspection PyMethodMayBeStatic
class TestTailgrams(object):
    def test_on_zero(self):
        assert list(tailgrams([])) == []

    def test_on_one(self):
        assert list(tailgrams([1])) == [((None,), 1)]

    def test_on_two(self):
        assert list(tailgrams([1, 2])) == [((None,), 1), ((1,), 2)]

    def test_on_three(self):
        assert list(tailgrams([1, 2, 3])) == [((None,), 1), ((1,), 2), ((2,), 3)]

    def test_on_four(self):
        assert list(tailgrams([1, 2, 3, 4])) == [((None,), 1), ((1,), 2), ((2,), 3), ((3,), 4)]

    def test_on_five_long_tail(self):
        print(list(tailgrams([1, 2, 3, 4, 5], 3)))

        assert list(tailgrams([1, 2, 3, 4, 5], 3)) == [
            ((None, None, None), 1),
            ((None, None, 1), 2),
            ((None, 1, 2), 3),
            ((1, 2, 3), 4),
            ((2, 3, 4), 5),
        ]


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class TestMatrixFeeding(object):
    def test_feed_simple(self):
        r = StringIO('ab')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.transition(('a',), 'b') == 1

    def test_feed_less_simple(self):
        r = StringIO('ababac')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.transitions(('a',)) == {
            'b': 2,
            'c': 1,
        }


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class TestWordGeneration(object):
    def test_choose_simple_transition(self):
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

    def test_choose_transition(self):
        trans = Matrix.choose_transition({
            'a': 1,
            'b': 1,
            'c': 1,
            False: 1,
            True: 1,
        }, 0.5)

        assert trans == 'c'

    def test_generate_simple_word(self):
        r = StringIO('abc')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.make_word() == 'abc'

    def test_generate_word(self):
        r = StringIO('bonjour youpi tralala pouet youpla')
        n = FrenchNormalizer(r)
        m = Matrix()

        m.feed(n)

        assert m.make_word(10) == 'tr'

    def test_deterministic(self):
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
