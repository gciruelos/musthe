musthe
======

Music theory implemented in Python. Notes, scales and chords. It was made as an experiment to test Python3, unit testing and magic methods.

It is still in development so feel free to read the code, fork and make pull requests! They are very welcome!


How to use
==========

It is very simple, everything is coded in a object-oriented style, for example:

    $ python -i musthe.py
    >>> a = Note('A')  #Default A4
    >>> a
    Note("A4")
    >>> str(a)
    'A'



Suppose you want to create tension, so you want the perfect fifth or the minor seventh of that A, so you do:

    >>> fifth = Interval('P5')
    >>> seventh = Interval('m7')
    >>> a+fifth
    Note("E5")
    >>> str(a+fifth)
    'E'
    >>> str(a+seventh)
    'G'

Though it is important to see that the octaves of those notes are different:

    >>> a.octave
    4
    >>> (a+seventh).octave
    5

Now lets try scales:

    >>> scale(Note('B'), 'major')
    [Note("B4"), Note("C#5"), Note("D#5"), Note("E5"), Note("F#5"), Note("G#5"), Note("A#5"), Note("B5")]

It return a list of Note instances, so if you want a cleaner result should do something like:

    >>> list(map(str, scale(Note('B'), 'major')))
    ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B']
    
Fair enough.

Basic triad (major, minor, diminished, augmented) support has been added.

Basic chord usage, default args return A Major:

	>>> musthe.Chord()
	A major chord: [Note("A4"), Note("C#5"), Note("E5")]
	>>> musthe.Chord('A', 'minor')
	A minor chord: [Note("A4"), Note("C5"), Note("E5")]
	>>> musthe.Chord('A', 'augmented')
	A augmented chord: [Note("A4"), Note("C#5"), Note("E#5")]
	>>> musthe.Chord('A', 'diminished')
	A diminished chord: [Note("A4"), Note("C5"), Note("Eb5")]

The chords contain an internal list (Chord-Object.notes) containing Note objects that make up the chord. 

If you have lilypond installed, you can make little melodies using this program, an example is given in 'lilypond_example.py'


Contributors
============

* [Sri Raghavan](https://github.com/srir)
* [David H](http://github.com/bobthenameless)
* [Sylvain](https://github.com/SylvainDe)

License
=======

See license file.

This was made by Gonzalo Ciruelos <gonzalo.ciruelos@gmail.com>


