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
	
	def test_note_scales(self):
		self.assertEqual(list(map(str, scale(Note('C'), 'major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, scale(Note('C'), 'major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, scale(Note('C'), 'major'))), ['C','D','E','F','G','A','B','C'])

if __name__ == '__main__':
    unittest.main()
