# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

import re

WORD_START = False
WORD_STOP = True
BLANK_WORD = [WORD_START]


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

    def words(self):
        w = list(BLANK_WORD)

        for c in self.chars():
            w.append(c)

            if c == WORD_STOP:
                yield w
                w = list(BLANK_WORD)


class FrenchNormalizer(Normalizer):
    FRENCH_CHAR = re.compile(r"^[a-z\-'àâçéêèëïîôœùûü]$")

    def __init__(self, *args, **kwargs):
        super(FrenchNormalizer, self).__init__(*args, **kwargs)
        self.in_word = False

    def next_char(self):
        while True:
            c = self.reader.read(1).lower()

            if c == '':
                if self.in_word:
                    self.in_word = False
                    return WORD_STOP
                else:
                    return None
            elif self.FRENCH_CHAR.match(c):
                self.in_word = True
                return c
            elif self.in_word:
                self.in_word = False
                return WORD_STOP
