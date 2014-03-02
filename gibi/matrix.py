# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals
import itertools
from bisect import bisect
from gibi.io import WORD_START, WORD_STOP
from six import StringIO, string_types
from random import Random


class Matrix(object):
    def __init__(self):
        self.dict = {}
        self.totals = {}
        self._seeded = False
        self._random = Random()

    def increment(self, src, dst):
        if src not in self.dict:
            self.dict[src] = {}
            self.totals[src] = 0

        if dst not in self.dict[src]:
            self.dict[src][dst] = 0

        self.dict[src][dst] += 1
        self.totals[src] += 1

    def transition(self, src, dst):
        if src in self.dict and dst in self.dict[src]:
            return self.dict[src][dst] / self.totals[src]
        else:
            return 0

    def transitions(self, src):
        output = {}

        for dst, _ in self.dict[src].items():
            output[dst] = self.transition(src, dst)

        return output

    def feed(self, normalizer):
        for word in normalizer.words():
            for x, y in bigrams(word):
                self.increment(x, y)

    @staticmethod
    def choose_transition(transitions, draw):
        """
        Chooses a transition for the given draw. It is completely deterministic.
        """

        class ComparableChoice(tuple):
            @staticmethod
            def char_cmp(self, other):
                """
                True < False < str
                """

                if (isinstance(self, string_types) and isinstance(other, bool)) \
                        or (self is False and other is True):
                    return True
                elif isinstance(self, string_types):
                    return self < other
                else:
                    return False

            def __lt__(self, other):
                if self[1] < other[1]:
                    return True
                elif self[1] == other[1]:
                    return self.char_cmp(self[0], other[0])
                else:
                    return False

        weighted_choices = sorted([ComparableChoice((x, y)) for x, y in transitions.items()])
        choices, weights = zip(*weighted_choices)
        sum_weight = list(itertools.accumulate(weights))
        return choices[bisect(sum_weight, draw)]

    def make_word(self, seed=None):
        if seed is not None or not self._seeded:
            self._random.seed(seed)

        with StringIO() as out:
            c = WORD_START

            while True:
                c = self.choose_transition(self.transitions(c), self._random.random())

                if c == WORD_STOP:
                    break
                else:
                    out.write(c)

            result = out.getvalue()

        return result


def bigrams(iterable):
    pos = 0
    tail = None

    for x in iterable:
        if pos > 0:
            yield (tail, x)

        pos += 1
        tail = x
