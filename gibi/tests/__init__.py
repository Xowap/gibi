# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from __future__ import unicode_literals

from os import path as _path
from sys import path as _sys_path

GIBI_ROOT = _path.realpath(_path.join(_path.dirname(_path.abspath(__file__)), '..', '..'))
_sys_path.append(GIBI_ROOT)

from .matrix import *
from .io import *
