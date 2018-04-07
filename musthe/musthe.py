#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2018
Gonzalo Ciruelos <gonzalo.ciruelos@gmail.com>
Federico Ferri <federico.ferri.it@gmail.com>
"""

import re


class Tone:
    """
    The tone class.

    There are 7 tones: C, D, E, F, G, A, and B.

    This class implements basic tone arithmetic, such as adding and
    subtracting interval numbers, or computing a difference between
    two tones.
    """

    tones = 'CDEFGAB'
    tones_idx = {x: i for i, x in enumerate(tones)}

    def __init__(self, tone):
        if tone not in self.tones_idx:
            raise ValueError('Invalid tone {!r}'.format(tone))
        self.name = tone
        self.idx = self.tones_idx[tone]

    def __add__(self, o):
        if isinstance(o, int):
            if o == 0:
                raise ValueError('Invalid interval number: 0')
            new_idx = (self.idx + o - (1 if o > 0 else -1)) % len(self.tones)
            return Tone(self.tones[new_idx])
        else:
            raise TypeError('Cannot add {} to Tone'.format(type(o)))

    def __sub__(self, o):
        if isinstance(o, Tone):
            d = self.idx - o.idx
            d += 1 if d >= 0 else -1
            return d
        elif isinstance(o, int):
            return self + -o
        else:
            raise TypeError('Cannot subtract {} from Tone'.format(type(o)))

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Tone({!r})'.format(str(self))


class Note:
    """
    The note class.

    The notes are to be parsed in th following way:
    * the letter name,
    * accidentals (up to 3),
    * octave (default is 4).

    For example, 'Ab', 'G9', 'B##7' are all valid notes. '#', 'A9b',
    'Dbbbb' are not.
    """

    pattern = re.compile(r'([A-G])(b{0,3}|#{0,3})(\d{0,1})$')
    tones = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    def __init__(self, note):
        m = self.pattern.match(note)
        if m is None: raise Exception('Could not parse the note {!r}'.format(note))

        self.tone = Tone(m.group(1))
        self.accidental = m.group(2)
        self.octave = int(m.group(3) or '4')

        self.note_id = self.tones[self.tone.name]
        for change in self.accidental:
            if change == '#': self.note_id += 1
            elif change == 'b': self.note_id -= 1
        self.note_id %= 12

    def __add__(self, interval):
        if not isinstance(interval, Interval):
            raise Exception('Cannot add {} to a note.'.format(type(interval)))

        new_tone = self.tone + interval.number

        new_note_id = (self.note_id + interval.semitones) % 12

        new_note_octave = (self.note_id + interval.semitones) // 12 + self.octave

        difference = new_note_id - self.tones[new_tone.name]
        if difference < 3: difference += 12
        if difference > 3: difference -= 12
        accidental = 'b' * max(0, -difference) + '#' * max(0, difference)

        # corrects cases like B#, B##, B### and A###.
        if new_tone.name + accidental in ['B#', 'B##', 'B###', 'A###']:
            new_note_octave -= 1

        return Note(new_tone.name + accidental + str(new_note_octave))

    def __sub__(self, interval):
        return self + -interval

    def midi_note(self):
        return self.note_id + self.octave * 12

    def frequency(self):
        from math import pow
        return 440.0 * pow(2, 1./12.)**(self.midi_note() - Note('A4').midi_note())

    def to_octave(self, octave):
        return Note(self.tone.name + self.accidental + str(octave))

    def lilypond_notation(self):
        return str(self).replace('b', 'es').replace('#', 'is').lower()

    def scientific_notation(self):
        return str(self) + str(self.octave)

    def __repr__(self):
        return 'Note({!r})'.format(self.scientific_notation())

    def __str__(self):
        return self.tone.name + self.accidental

    def __eq__(self, other):
        return self.scientific_notation() == other.scientific_notation()


class Interval:
    """
    The interval class.

    The intervals are to be parsed in th following way:
    * the quality, (m, M, p, A, d)
    * the number.

    For example, 'd8', 'P1', 'A5' are valid intervals. 'P3', '5' are not.
    """

    intervals = {
                            'P1': 0,            'A1': 1,
        'd2': 0,  'm2': 1,            'M2': 2,  'A2': 3,
        'd3': 2,  'm3': 3,            'M3': 4,  'A3': 5,
        'd4': 4,            'P4': 5,            'A4': 6,
        'd5': 6,            'P5': 7,            'A5': 8,
        'd6': 7,  'm6': 8,            'M6': 9,  'A6': 10,
        'd7': 9,  'm7': 10,           'M7': 11, 'A7': 12,
        'd8': 11,           'P8': 12,           'A8': 13,
    }

    def __init__(self, interval):
        self.quality = interval[0]
        self.number = int(interval[1:])
        self.semitones = 0

        # compound intervals:
        number = self.number
        while number > 8:
            number -= 7
            self.semitones += 12
        interval1 = self.quality + str(number)

        try:
            self.semitones = self.intervals[interval1]
        except:
            raise Exception('Invalid interval {!r}.'.format(interval))

    def __str__(self):
        return self.quality + str(self.number)

    def __repr__(self):
        return 'Interval({!r})'.format(str(self))

    def __neg__(self):
        i = Interval(self.quality + str(self.number))
        i.number *= -1
        i.semitones *= -1
        return i


class Chord:
    """
    The chord class.

    Contains recipes for common chords.
    """

    recipes = {
        'maj':    ['P1', 'M3', 'P5'],
        'min':    ['P1', 'm3', 'P5'],
        'aug':    ['P1', 'M3', 'A5'],
        'dim':    ['P1', 'm3', 'd5'],
        'dom7':   ['P1', 'M3', 'P5', 'm7'],
        'min7':   ['P1', 'm3', 'P5', 'm7'],
        'maj7':   ['P1', 'M3', 'P5', 'M7'],
        'aug7':   ['P1', 'M3', 'A5', 'm7'],
        'dim7':   ['P1', 'm3', 'd5', 'd7'],
        'm7dim5': ['P1', 'm3', 'd5', 'm7'],
        'sus2':   ['P1', 'P5', 'P8', 'M2'],
        'sus4':   ['P1', 'P5', 'P8', 'P4'],
        'open5':  ['P1', 'P5', 'P8'],
    }
    aliases = {
        'M':      'maj',
        'm':      'min',
        '+':      'aug',
        '°':      'dim',
        '7':      'dom7',
        'm7':     'min7',
        'M7':     'maj7',
        '+7':     'aug7',
        '7aug5':  'aug7',
        '7#5':    'aug7',
        '°7':     'm7dim5',
        'ø7':     'm7dim5',
        'm7b5':   'm7dim5',
    }
    valid_types = list(recipes.keys()) + list(aliases.keys())

    def __init__(self, root, chord_type='M'):
        if isinstance(root, str):
            for s in sorted(self.valid_types, key=lambda x: -len(x)):
                if root.endswith(s):
                    chord_type = s
                    root = Note(root[:-len(s)])
                    break
            if not isinstance(root, Note):
                raise ValueError('Invalid chord: {!r}'.format(root))

        if chord_type in self.aliases:
            chord_type = self.aliases[chord_type]
        if chord_type not in self.recipes.keys():
            raise Exception('Invalid chord type supplied. Valid types: {}.'.format(' '.join(self.valid_types)))

        self.chord_type = chord_type
        self.notes = [root + Interval(i) for i in self.recipes[chord_type]]

    def __repr__(self):
        return "Chord({!r}, {!r})".format(self.notes[0], self.chord_type)

    def __str__(self):
        return "{}{}".format(str(self.notes[0]), self.chord_type)

    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            #if chords dont have the same number of notes, def not equal
            return False
        else:
            return all(self.notes[i] == other.notes[i] for i in range(len(self.notes)))

class Scale:
    """
    The scale class.

    Contains recipes for common scales, and operators for accessing the
    notes of the scale, and for checking if a scale contains specific
    notes or chords.
    """

    scales = {
        'major' :           ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7'],
        'natural_minor':    ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'm7'],
        'harmonic_minor':   ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'M7'],
        'melodic_minor':    ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'M7'],
        'dorian':           ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'm7'],
        'locrian':          ['P1', 'm2', 'm3', 'P4', 'd5', 'm6', 'm7'],
        'lydian':           ['P1', 'M2', 'M3', 'A4', 'P5', 'M6', 'M7'],
        'mixolydian':       ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'm7'],
        'phrygian':         ['P1', 'm2', 'm3', 'P4', 'P5', 'm6', 'm7'],
        'major_pentatonic': ['P1', 'M2', 'M3',       'P5', 'M6'],
        'minor_pentatonic': ['P1',       'm3', 'P4', 'P5',       'm7']
    }

    def all():
        for note in Note.tones:
            for accidental in ('b', '', '#'):
                root = Note(note + accidental)
                for name in Scale.scales:
                    yield Scale(root, name)

    def __init__(self, root, name):
        if isinstance(root, str):
            root = Note(root)

        if not isinstance(root, Note):
            raise TypeError('Invalid root note type: {}'.format(type(root)))
        if name not in self.scales:
            raise NameError('No such scale: {}'.format(name))
        self.root = root
        self.name = name
        self.intervals = [Interval(i) for i in self.scales[name]]
        self.notes = [(root + i).to_octave(0) for i in self.intervals]

    def __getitem__(self, k):
        if isinstance(k, int):
            try:
                octaves = k // len(self)
                offset = k - octaves * len(self)
                return self.root.to_octave(self.root.octave + octaves) + self.intervals[offset]
            except:
                raise IndexError('Index out of range')
        elif isinstance(k, slice):
            return [self[i] for i in range(k.start or 0, k.stop or self.max_index, k.step or 1)]
        else:
            raise TypeError('Scale cannot be indexed by {}.'.format(type(k)))

    def __len__(self):
        return len(self.intervals)

    def __contains__(self, k):
        if isinstance(k, Note):
            return k.to_octave(0) in self.notes
        elif isinstance(k, Chord):
            return all(n in self for n in k.notes)
        elif isinstance(k, (list, set, tuple)):
            return all(x in self for x in k)
        else:
            raise TypeError('Cannot check scale containment for an object of type {}'.format(type(k)))

    def __str__(self):
        return '{} {}'.format(self.root, self.name)

    def __repr__(self):
        return 'Scale({!r}, {!r})'.format(self.root, self.name)


if __name__ == '__main__':
    add = Note('Ab') + Interval('m3')
    print(add)
