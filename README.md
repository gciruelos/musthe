musthe
======

Music theory implemented in Python. Notes, scales and chords.

It is still in development so feel free to read the code, fork and make pull requests! They are very welcome!

Installation
============

To install:

    $ pip install musthe


Development install
===================

To install as development:

(Optional) Create a virtualenv:

    $ python -m venv env
    $ source env/bin/activate

Then install:

    $ pip install -e .


How to use
==========

It is very simple, everything is coded in a object-oriented style, for example:

    $ python
    >>> from musthe import *
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

Now let's see basic chord usage:

	>>> Chord(Note('A'), 'M')
	Chord(Note('A'), 'M')
	>>> Chord(Note('A'), 'M').notes
	[Note("A4"), Note("C#5"), Note("E5")]
	>>> Chord(Note('Bb'), 'dim').notes
	[Note("Bb4"), Note("Db5"), Note("Fb5")]

You can use a string to construct a chord:

    >>> Chord('C#aug7') == Chord(Note('C#'), 'aug7')
    True

Default chord type is 'M' (Major).

Now lets try scales:

    >>> s = Scale(Note('B'), 'major')
    >>> [s[i] for i in range(len(s))]
    [Note('B4'), Note('C#5'), Note('D#5'), Note('E5'), Note('F#5'), Note('G#5'), Note('A#5')]
    >>> s[0]
    Note('B4')
    >>> s[-11]
    Note('E3')

It return a list of Note instances, so if you want a cleaner result should do something like:

    >>> s = Scale(Note('B'), 'major')
    >>> [str(s[i]) for i in range(len(s))]
    ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']

To check if notes and chords are contained in a given scale:

    >>> Note('D#3') in s
    True
    >>> Note('F3') in s
    False
    >>> Chord('C#m') in s
    True
    >>> Chord('CM') in s
    False

Now let's try some advanced stuff: given a list of chords, find all scales that contain those:

    >>> chords = [Chord('Cm'), Chord('Fm7'), Chord('Gm')]
    >>> for scale in Scale.all():
    ...     if chords in scale:
    ...         print(scale)
    ...
    C natural_minor
    Eb major

Conversely, given a scale, you can use the `harmonize` method to find all of the
diatonic and dominant 7th chords for reach note in that scale:

    >>> from pprint import pprint
    ... scale = Scale('C', 'major')
    ... pprint(scale.harmonize(), indent=2)
    [ [ Chord(Note('C4'), 'maj'),
        Chord(Note('C4'), 'dom7'),
        Chord(Note('C4'), 'maj7'),
        Chord(Note('C4'), 'sus2'),
        Chord(Note('C4'), 'sus4'),
        Chord(Note('C4'), 'open5'),
        Chord(Note('C4'), 'dom9'),
        Chord(Note('C4'), 'maj9')],
    [ Chord(Note('D4'), 'min'),
        Chord(Note('D4'), 'min7'),
        Chord(Note('D4'), 'sus2'),
        Chord(Note('D4'), 'sus4'),
        Chord(Note('D4'), 'open5'),
        Chord(Note('D4'), 'min9')],
    [ Chord(Note('E4'), 'min'),
        Chord(Note('E4'), 'min7'),
        Chord(Note('E4'), 'sus4'),
        Chord(Note('E4'), 'open5')],
    [ Chord(Note('F4'), 'maj'),
        Chord(Note('F4'), 'dom7'),
        Chord(Note('F4'), 'maj7'),
        Chord(Note('F4'), 'sus2'),
        Chord(Note('F4'), 'open5'),
        Chord(Note('F4'), 'dom9'),
        Chord(Note('F4'), 'maj9')],
    [ Chord(Note('G4'), 'maj'),
        Chord(Note('G4'), 'dom7'),
        Chord(Note('G4'), 'sus2'),
        Chord(Note('G4'), 'sus4'),
        Chord(Note('G4'), 'open5'),
        Chord(Note('G4'), 'dom9')],
    [ Chord(Note('A4'), 'min'),
        Chord(Note('A4'), 'min7'),
        Chord(Note('A4'), 'sus2'),
        Chord(Note('A4'), 'sus4'),
        Chord(Note('A4'), 'open5'),
        Chord(Note('A4'), 'min9')],
    [ Chord(Note('B4'), 'dim'),
        Chord(Note('B4'), 'm7dim5')] ]

(If you prefer to omit dominant 7th chords you can use `harmonize(include_dom7=False)`. You can also use the `harmonize_dict` method to get a dictionary instead of a list, with a key for each note in the scale.)


If you have [lilypond](http://lilypond.org/) installed, you can make little melodies using this program, an example is given in 'lilypond_example.py'

Running Tests
=============

From the project root directory, run:

```
python -m tests.tests
```

Contributors
============

* [zsinx6](https://github.com/zsinx6)
* [Federico Ferri](https://github.com/fferri)
* [Gonzalo Ciruelos](https://github.com/gciruelos)
* [David H](https://github.com/bobthenameless)
* [nvoster](https://github.com/nvoster)
* [Sylvain](https://github.com/SylvainDe)
* [Edgar Gavrik](https://github.com/edgarasg)
* [Sri Raghavan](https://github.com/srir)
* [Augustus Wynn](https://github.com/guswynn)
* [Marco Heins](https://github.com/barrio)
* [Andy Chase](https://github.com/mystery-house)


License
=======

See license file.
