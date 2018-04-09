
import unittest
from musthe import *


class TestsForJesus(unittest.TestCase):
    def test_note_parsing(self):
        self.assertEqual(str(Note('A4')), 'A')
        self.assertEqual(str(Note('Ab6')), 'Ab')
        self.assertEqual(str(Note('Dbb')), 'Dbb')
        self.assertEqual(str(Note('G###0')), 'G###')

        self.assertRaises(Exception, Note, 'A99')
        self.assertRaises(Exception, Note, 'Ab#')
        self.assertRaises(Exception, Note, 'E####')

    def test_interval_parsing(self):
        self.assertEqual(Interval('d5').semitones, 6)
        self.assertRaises(Exception, Interval, 'P3')

    def test_note_sum(self):
        self.assertEqual(str(Note('A4')+Interval('d5')), str(Note('Eb')))
        self.assertEqual(str(Note('A')+Interval('P1')), str(Note('A')))
        self.assertEqual(str(Note('G##')+Interval('m3')), str(Note('B#')))
        self.assertEqual(str(Note('F')+Interval('P5')), str(Note('C')))

    def test_tone_arithmetic(self):
        self.assertEqual(str(Tone('A')+2), 'B')
        self.assertEqual(str(Tone('A')+3), 'C')
        self.assertEqual(str(Tone('A')+5), 'E')
        self.assertEqual(str(Tone('G')+11), 'C')
        self.assertEqual(str(Tone('D')+1), 'D')
        self.assertEqual(str(Tone('D')-2), 'C')
        self.assertEqual(Tone('D')-Tone('C'), 2)

    def test_intercval_arithmetic(self):
        for x, y in {
            'P1': 'P8',
            'A1': 'd8',
            'd2': 'A7',
            'm2': 'M7',
            'M2': 'm7',
            'A2': 'd7',
            'd3': 'A6',
            'm3': 'M6',
            'M3': 'm6',
            'A3': 'd6',
            'd4': 'A5',
            'P4': 'P5',
            'A4': 'd5',
            'd5': 'A4',
            'P5': 'P4',
            'A5': 'd4',
            'd6': 'A3',
            'm6': 'M3',
            'M6': 'm3',
            'A6': 'd3',
            'd7': 'A2',
            'm7': 'M2',
            'M7': 'm2',
            'A7': 'd2',
            'd8': 'A1',
            'P8': 'P1',#unnorm
            'A8': 'd8',#unnorm
        }.items():
            i = Interval(x)
            c = i.complement()
            self.assertEqual(str(c), y)
            c4, c5 = Note('C4'), Note('C5')
            if x != 'A8':
                self.assertEqual(c4 + i + c, c5)

    def test_note_scales(self):
        self.assertEqual(list(map(str, Scale(Note('C'), 'major').notes)),          ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'natural_minor').notes)),  ['C', 'D', 'Eb','F', 'G', 'Ab','Bb'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'harmonic_minor').notes)), ['C', 'D', 'Eb','F', 'G', 'Ab','B'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'melodic_minor').notes)),  ['C', 'D', 'Eb','F', 'G', 'A', 'B'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'dorian').notes)),         ['C', 'D', 'Eb','F', 'G', 'A', 'Bb'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'locrian').notes)),        ['C', 'Db','Eb','F', 'Gb','Ab','Bb'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'lydian').notes)),         ['C', 'D', 'E', 'F#','G', 'A', 'B'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'mixolydian').notes)),     ['C', 'D', 'E', 'F', 'G', 'A', 'Bb'])
        self.assertEqual(list(map(str, Scale(Note('C'), 'phrygian').notes)),       ['C', 'Db','Eb','F', 'G', 'Ab','Bb'])
        self.assertEqual(list(map(str, Scale(Note('C'),'major_pentatonic').notes)),['C', 'D', 'E', 'G', 'A'])
        self.assertEqual(list(map(str, Scale(Note('C'),'minor_pentatonic').notes)),['C', 'Eb','F', 'G', 'Bb'])
        self.assertRaises(Exception, Scale, Note('C'), 'non-existent scale')
        # try to create all scales
        for scale in Scale.all():
            pass

class TestsForJesusChords(unittest.TestCase):
    def setUp(self):
        '''put here for later building of test chords, one for each
        chord_type in chord_recipes'''
        self.chord_types = [k for k in Chord(Note('Bb')).recipes.keys()]
        self.chords = {k:Chord(Note('A'), k) for k in self.chord_types}
        self.rootNote = Note('A')

    def tearDown(self):
        self.chords = {}
        self.chord_types = []
        self.rootNote = None

    def test_chord_creation(self):
        #check __str__ returns
        self.assertEqual(str(Chord(Note('A'))), 'Amaj')
        self.assertEqual(str(Chord(Note('B'), 'm')), 'Bmin')
        self.assertEqual(str(Chord(Note('C'), 'dim')), 'Cdim')
        self.assertEqual(str(Chord(Note('D'), 'aug')), 'Daug')
        self.assertEqual(str(Chord(Note('A#'))), 'A#maj')
        self.assertEqual(str(Chord(Note('Bb'))), 'Bbmaj')

        #check __repr__ returns
        #//todo
        
        #check __eq__
        #//todo

        #check faulty inputs
        self.assertRaises(Exception, Chord, 'A$')
        self.assertRaises(Exception, Chord, 'H')

        #check recipe notes
        self.assertEqual(self.chords['maj'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('M3'),
                          self.rootNote+Interval('P5')
                          ])
        self.assertEqual(self.chords['min'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('m3'),
                          self.rootNote+Interval('P5')
                          ])
        self.assertEqual(self.chords['dim'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('m3'),
                          self.rootNote+Interval('d5')
                          ])
        self.assertEqual(self.chords['aug'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('M3'),
                          self.rootNote+Interval('A5')
                          ])

unittest.main()
