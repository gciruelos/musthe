musthe
======

Music theory implemented in Python. Notes, scales and chords.

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

    >>> s = Scale(Note('B'), 'major')
    >>> [s[i] for i in range(len(s))]
    [Note('B4'), Note('C#5'), Note('D#5'), Note('E5'), Note('F#5'), Note('G#5'), Note('A#5')]
    >>> s[0]
    Note('B4')
    >>> s[-11]
    Note('E3')

To check if notes and chords are contained in a given scale:

    >>> Note('D#3') in s
    True
    >>> Note('F3') in s
    False
    >>> Chord(Note('C#'), 'm') in s
    True
    >>> Chord(Note('C'), 'M') in s
    False

It return a list of Note instances, so if you want a cleaner result should do something like:

    >>> s = Scale(Note('B'), 'major')
    >>> [str(s[i]) for i in range(len(s))]
    ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
    
Fair enough.

Now with let's see basic chord usage:

	>>> Chord(Note('A'), 'M')
	Chord(Note('A'), 'M')
	>>> Chord(Note('A'), 'M').notes
	[Note("A4"), Note("C#5"), Note("E5")]
	>>> Chord(Note('Bb'), 'dim').notes
	[Note("Bb4"), Note("Db5"), Note("Fb5")]

Default chord type is 'M' (Major). Currently, only triads (major, minor, diminished, augmented) are supported.

Now let's try some advanced stuff: given a list of chords, find all scales that contain them:

    >>> chords = [Chord(Note('C'), 'm'), Chord(Note('F'), 'm7'), Chord(Note('G'), 'm')]
    >>> for scale in Scale.all():
    ...     if all(chord in scale for chord in chords):
    ...         print(scale)
    ...
    C natural_minor
    D locrian
    Eb major
    F dorian
    G phrygian
    Ab lydian
    Bb mixolydian


If you have lilypond installed, you can make little melodies using this program, an example is given in 'lilypond_example.py'


Contributors
============

In alphabetical order

* [David H](https://github.com/bobthenameless)
* [Edgar Gavrik](https://github.com/edgarasg)
* [Federico Ferri](https://github.com/fferri)
* [Marco Heins](https://github.com/barrio)
* [Sri Raghavan](https://github.com/srir)
* [Sylvain](https://github.com/SylvainDe)


License
=======

See license file.

This was made by Gonzalo Ciruelos <gonzalo.ciruelos@gmail.com>


