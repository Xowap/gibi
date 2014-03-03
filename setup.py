# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Gibi
# (c) 2014 Rémy Sanchez <remy.sanchez@activkonnect.com>
# Released under the terms of the WTFPL

from distutils.core import setup
from os import path as _path
from sys import path as _sys_path

import codecs

GIBI_ROOT = _path.realpath(_path.join(_path.dirname(_path.abspath(__file__))))
_sys_path.append(GIBI_ROOT)

with codecs.open(_path.join(GIBI_ROOT, 'README.rst'), 'r', 'utf-8') as f:
    long_description = f.read()

with codecs.open(_path.join(GIBI_ROOT, 'requirements.txt'), 'r', 'utf-8') as f:
    requirements = [x.strip() for x in f.readlines() if not x.startswith('tox')]

setup(
    name='gibi',
    version='0.2.1',
    author='Rémy Sanchez',
    author_email='remy.sanchez@hyperthese.net',
    packages=['gibi', 'gibi.tests'],
    scripts=['bin/gibi'],
    url='https://github.com/Xowap/gibi',
    license='COPYING.txt',
    description='Generate random words based on Markov chains',
    long_description=long_description,
    install_requires=requirements,
)
