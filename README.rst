Gibi
====

Gibi is a random word generator, based on Markov chains.

It analyzes a text in order to deduce the probability of transition from one
character to another, and then generates a completely random word that will look
alike what you have feeded it as input.

Build status
------------

.. |build-develop| image:: https://travis-ci.org/Xowap/gibi.png?branch=develop
.. _build-develop: https://travis-ci.org/Xowap/gibi

.. |build-master| image:: https://travis-ci.org/Xowap/gibi.png?branch=master
.. _build-master: https://travis-ci.org/Xowap/gibi

:develop: |build-develop|_
:master: |build-master|_

Usage
-----

Gibi can be used either as a CLI tool, either as a library.

CLI
~~~

A tool named `gibi` helps you to generate a matrix file, and then use it to generate words. It is
self-documented using the `--help` switch, however here is a typical workflow.

.. code-block::

   $ gibi analyze corpus.txt matrix.gibi
   $ gibi generate matrix.gibi

This will analyze the `corpus.txt` file into the `matrix.gibi` file, and then produce 10 random
words.

API
~~~

Basic usage
...........

In its simplest form, using the API looks like:

.. code-block:: python

   with codecs.open(path, 'r', encoding='utf-8') as f:
       n = FrenchNormalizer(f)
       m = Matrix()

       m.feed(n)

   print(m.make_word())

You can also make something deterministic by providing a seed to `make_word()`.
Given the same `Matrix` and the same seed, you will always get the same result.
The provided seed is anything that `Python's random <http://docs.python.org/3.3/library/random.html#random.seed>`_
would accept. See the following example:

.. code-block:: python

   assert m.make_word(42) == m.make_word(42)

Using matrix files
..................

You will probably pre-generate a matrix file using `gibi analyze`, and then load the resulting file
like this

.. code-block:: python

   m = Matrix()
   with open('matrix.gibi', 'rb') as f:
       m.load(f)

   print(m.make_word())

This is much more performant, as generating the matrix can be time-consuming if the corpus is big.

Legal terms
-----------

This project is written and copyrighted by its authors, as the Git log can
testify.

It is released under the terms of the WTFPL. Please refer to the COPYING file
for more information.
