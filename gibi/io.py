# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

import re

WORD_START = False
WORD_STOP = True


class Normalizer(object):
    def __init__(self, reader):
        self.reader = reader

    def next_char(self):
        raise NotImplementedError

    def chars(self):
        while True:
            c = self.next_char()

            if c is not None:
                yield c
            else:
                break


class FrenchNormalizer(Normalizer):
    FRENCH_CHAR = re.compile(r"^[a-z\-'àâçéêèëïîœùûü]$")

    def __init__(self, *args, **kwargs):
        super(FrenchNormalizer, self).__init__(*args, **kwargs)
        self.in_word = False

    def next_char(self):
        while True:
            c = self.reader.read(1).lower()

            if c == '':
                return None
            elif self.FRENCH_CHAR.match(c):
                self.in_word = True
                return c
            elif self.in_word:
                self.in_word = False
                return WORD_STOP
