# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals


class Matrix(object):
    def __init__(self):
        self.dict = {}
        self.totals = {}

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
