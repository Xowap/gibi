# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals
import operator
import pickle
from bisect import bisect
from gibi.io import WORD_START, WORD_STOP
from six import StringIO, string_types
from random import Random


def accumulate(iterable, func=operator.add):
    """
    Return running totals. From Python doc.
    """
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total


class MatrixError(Exception):
    pass


class Matrix(object):
    def __init__(self, tail=1):
        self.dict = {}
        self.tail = tail
        self._seeded = False
        self._random = Random()

    def dump(self, writer):
        pickle.dump(self.dict, writer)

    def load(self, reader):
        self.dict = pickle.load(reader)

        for src, _ in self.dict.items():
            self.tail = len(src)
            break

    def increment(self, src, dst):
        if src not in self.dict:
            self.dict[src] = {}

        if dst not in self.dict[src]:
            self.dict[src][dst] = 0

        self.dict[src][dst] += 1

    def transition(self, src, dst):
        if src in self.dict and dst in self.dict[src]:
            return self.dict[src][dst]
        else:
            return 0

    def transitions(self, src):
        output = {}

        for dst, _ in self.dict[src].items():
            output[dst] = self.transition(src, dst)

        return output

    def feed(self, normalizer):
        for word in normalizer.words():
            for x, y in tailgrams(word, self.tail):
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
        sum_weight = list(accumulate(weights))
        return choices[bisect(sum_weight, draw * sum_weight[-1])]

    def make_word(self, seed=None, min=3, max=30, tries=100):
        if seed is not None or not self._seeded:
            self._random.seed(seed)

        out = StringIO()
        tail = CircularBuffer(self.tail)
        tail.append(WORD_START)

        while True:
            c = self.choose_transition(self.transitions(tail.tuple()), self._random.random())

            if c == WORD_STOP:
                break
            else:
                out.write(c)
                tail.append(c)

        result = out.getvalue()
        out.close()

        if min <= len(result) <= max:
            return result
        elif tries > 0:
            return self.make_word(seed, min, max, tries - 1)
        else:
            raise MatrixError


class CircularBuffer(object):
    """
    Stores data in a fixed-size circular buffer.
    """

    def __init__(self, size, default_value=None):
        self.buffer = [default_value] * size
        self.size = size
        self.pos = 0

    def append(self, value):
        """
        Appends some data at the end of the buffer, and automatically deletes
        the oldest value.
        """

        self.buffer[self.pos] = value
        self.pos = (self.pos + 1) % self.size

    def tuple(self):
        """
        Returns the current state of the buffer as a tuple.
        """

        return tuple(self.buffer[self.pos:] + self.buffer[:self.pos])


def tailgrams(iterable, tail=1):
    buffer = CircularBuffer(tail)

    for x in iterable:
        yield (buffer.tuple(), x)
        buffer.append(x)
