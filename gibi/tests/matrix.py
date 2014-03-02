# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

from gibi import Matrix


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
