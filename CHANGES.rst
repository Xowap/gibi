Gibi Changelog
==============

v0.2.3, 2014-03-06 – Stupid packaging issues
--------------------------------------------

Just fixing an idiotic packaging issue, no code change.

v0.2.2, 2014-03-03 – Binding words length
-----------------------------------------

A new option is introduced in order to bind words length. The default is to
generate a word that is comprised between 3 and 30 characters long.

v0.2.1, 2014-03-03 – Forgotten character
----------------------------------------

The french character "ô" was not recognized as a proper letter.

v0.2.0, 2014-03-03 – Tooling
----------------------------

* A new `gibi` command, that handles both matrix file generation and random
  word generation.
* The possibility to calculate transitions from "tails": instead of just
  looking at the last character, look at the N last characters. I guess this
  a bit less like Markov chains. Who cares, it gives much better results.


v0.1.1, 2014-03-02 – Packaging
------------------------------

No functional change, however now Gibi is now fully packaged. Yay :)

v0.1.0, 2014-03-02 – Initial Release
------------------------------------

Initial release, features include

* Create a Markov chain from a french text, based on the transitions from one
  letter to the other.
* Generate a random word based on that chain. The generation can be seeded so
  the output is deterministic.
