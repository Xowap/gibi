#!/usr/bin/env python
# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from sys import argv
import codecs
from gibi.io import FrenchNormalizer
from gibi.matrix import Matrix


if __name__ == '__main__':
    path = argv[1]

    with codecs.open(path, 'r', encoding='utf-8') as f:
        n = FrenchNormalizer(f)
        m = Matrix()

        m.feed(n)

    print(m.make_word())
