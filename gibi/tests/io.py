# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals
from gibi.io import Normalizer, FrenchNormalizer, WORD_START, WORD_STOP
from nose.tools.nontrivial import raises
from six import StringIO


# noinspection PyMethodMayBeStatic
class TestIO(object):
    @raises(NotImplementedError)
    def test_normalizer_bare(self):
        r = StringIO()
        n = Normalizer(r)
        n.next_char()

    def test_normalizer_iteration(self):
        class MockNormalizer(Normalizer):
            def __init__(self, *args, **kwargs):
                super(MockNormalizer, self).__init__(*args, **kwargs)
                self.i = 0

            def next_char(self):
                if self.i < 10:
                    self.i += 1
                    return chr(ord('a') - 1 + self.i)

        assert "".join(MockNormalizer(None).chars()) == 'abcdefghij'

    def test_normalize_french(self):
        src = "L'Éléphant a... La main sur le cœur!!!"
        dst = "l'éléphant a la main sur le cœur "

        r = StringIO(src)

        assert "".join([x if x is not True else ' ' for x in FrenchNormalizer(r).chars()]) == dst

    def test_get_words(self):
        src = "L'Éléphant a... La main sur le cœur"
        dst = [[WORD_START] + list(x) + [WORD_STOP]
               for x in "l'éléphant a la main sur le cœur".split(' ')]

        r = StringIO(src)

        assert list(FrenchNormalizer(r).words()) == dst
