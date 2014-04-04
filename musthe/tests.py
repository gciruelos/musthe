#!/usr/bin/env python   
# -*- coding: utf-8 -*-

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



'''TODO: FAILS TESTS DUE TO RELOCATION OF SCALES TO GLOBAL scales() function!
def test_note_scales(self):
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])
'''

class TestsForJesusChords(unittest.TestCase):
    def setUp(self):
        '''put here for later building of test chords, one for each
        chord_type in chord_recipes'''
        self.chord_types = [k for k in Chord().chord_recipes.keys()]
        self.chords = {k:Chord(Note('A'), k) for k in self.chord_types}
        self.rootNote = Note('A')

    def tearDown(self):
        self.chords = {}
        self.chord_types = []
        self.rootNote = None

    def test_chord_creation(self):
        #check __str__ returns
        self.assertEqual(str(Chord(Note('A'))), 'AM')
        self.assertEqual(str(Chord(Note('B'), 'm')), 'Bm')
        self.assertEqual(str(Chord(Note('C'), 'dim')), 'Cdim')
        self.assertEqual(str(Chord(Note('D'), 'aug')), 'Daug')
        self.assertEqual(str(Chord(Note('A#'))), 'A#M')
        self.assertEqual(str(Chord(Note('Bb'))), 'BbM')

        #check __repr__ returns
        #//todo

        #check __eq__
        self.assertEqual(Chord(), Chord(Note('A'), 'M'))

        #check faulty inputs
        self.assertRaises(Exception, Chord, 'A$')
        self.assertRaises(Exception, Chord, 'H')

        #check recipe notes
        self.assertEqual(self.chords['M'].notes,
                         [self.rootNote,
                          self.rootNote+Interval('M3'),
                          self.rootNote+Interval('P5')
                          ])
        self.assertEqual(self.chords['m'].notes,
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
