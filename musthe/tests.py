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
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])
		self.assertEqual(list(map(str, Note('C').scale('major'))), ['C','D','E','F','G','A','B','C'])

	def test_chord_parsing(self):
        	self.e_major = Chord('E', 'major')
        	self.a_minor = Chord('A', 'minor')
        	self.d_dim = Chord('D', 'diminished')
        	self.c_aug = Chord('C', 'augmented')


		self.assertEqual(map(str,self.e_major.notes), [
            			  str(Note('E')),
                          str(Note('G#')),
                          str(Note('B'))])
		self.assertEqual(map(str,self.a_minor.notes), [
                          str(Note('A')),
                          str(Note('C')),
                          str(Note('E'))])

		self.assertEqual(map(str,self.d_dim.notes), [
                          str(Note('D')),
                          str(Note('F')),
                          str(Note('Ab'))])

		self.assertEqual(map(str,self.c_aug.notes), [
                          str(Note('C')),
                          str(Note('E')),
                          str(Note('G#'))])



unittest.main()
