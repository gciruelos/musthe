import unittest
from musthe import *


class TestsForTone(unittest.TestCase):
    def test_tone_parsing(self):
        def test1(name):
            self.assertEqual(str(Tone(name)), name)
        for name in 'CDEFGAB':
            test1(name)

        def test2(badname):
            self.assertRaises(ValueError, Tone, badname)
        test2('C#')
        test2('Db')
        test2('H')
        test2('$')

    def test_tone_stuff(self):
        for i in 'DEGAB':
            self.assertTrue(Tone(i).has_flat())
        for i in 'CDFGA':
            self.assertTrue(Tone(i).has_sharp())

    def test_tone_arithmetic(self):
        def test1(tone, difference, result):
            self.assertEqual(str(Tone(tone) + difference), result)
        test1('A', 2, 'B')
        test1('A', 3, 'C')
        test1('A', 5, 'E')
        test1('G', 11, 'C')
        test1('D', 1, 'D')
        test1('D', -2, 'C')

        def test2(tone1, tone2, difference):
            self.assertEqual(Tone(tone1) - Tone(tone2), difference)
        test2('D', 'C', 2)
        test2('C', 'B', -7)

        def test3(tone1, difference, tone2):
            self.assertEqual(Tone(tone1) - difference, Tone(tone2))
        test3('D', 2, 'C')
        test3('C', 2, 'B')


class TestsForNote(unittest.TestCase):
    def test_note_parsing(self):
        def test1(note, strnote):
            self.assertEqual(str(Note(note)), strnote)
        test1('A4', 'A')
        test1('Ab6', 'Ab')
        test1('Dbb', 'Dbb')
        test1('G###0', 'G###')

        def test2(badnote):
            self.assertRaises(Exception, Note, badnote)
        test2('A99')
        test2('Ab#')
        test2('E####')

    def test_note_gen(self):
        self.assertEqual([n.scientific_notation() for n in Note.all(4,5)],
            ['C4', 'C#4', 'Db4', 'D4', 'D#4', 'Eb4', 'E4', 'F4', 'F#4',
                'Gb4', 'G4', 'G#4', 'Ab4', 'A4', 'A#4', 'Bb4', 'B4', 'C5',
                'C#5', 'Db5', 'D5', 'D#5', 'Eb5', 'E5', 'F5', 'F#5', 'Gb5',
                'G5', 'G#5', 'Ab5', 'A5', 'A#5', 'Bb5', 'B5'])

    def test_note_oct(self):
        def test1(n1, oc, n2):
            self.assertEqual(Note(n1).to_octave(oc), Note(n2))
        test1('C#2', 5, 'C#5')
        test1('B#6', 3, 'B#3')
        test1('Cbbb6', 6, 'Cbbb6')
        test1('Ebb5', 1, 'Ebb1')

    def test_note_midi(self):
        def test1(note, midi):
            self.assertEquals(Note(note).midi_note(), midi)
        test1('C4', 60)
        test1('D5', 74)

    def test_note_sum(self):
        def test1(note, interval, result):
            self.assertEqual(Note(note) + Interval(interval), Note(result))
        test1('A4', 'd5', 'Eb5')
        test1('A4', 'P1', 'A4')
        test1('G##4', 'm3', 'B#4')
        test1('F3', 'P5', 'C4')
        test1('B#4', 'd2', 'C5')


class TestsForInterval(unittest.TestCase):
    def test_interval_parsing(self):
        def test1(interval, semitones, number):
            i = Interval(interval)
            self.assertEqual(i.semitones, semitones)
            self.assertEqual(i.number, number)
        test1('d5', 6, 5)
        test1('P8', 12, 8)
        test1('A8', 13, 8)

        def test2(badinterval):
            self.assertRaises(Exception, Interval, badinterval)
        test2('P3')

    def test_interval_complement(self):
        def test1(i, c):
            i = Interval(i)
            c = Interval(c)
            self.assertEqual(i.complement(), c)
        test1('P1', 'P8')
        test1('A1', 'd8')
        test1('d2', 'A7')
        test1('m2', 'M7')
        test1('M2', 'm7')
        test1('A2', 'd7')
        test1('d3', 'A6')
        test1('m3', 'M6')
        test1('M3', 'm6')
        test1('A3', 'd6')
        test1('d4', 'A5')
        test1('P4', 'P5')
        test1('A4', 'd5')
        test1('d5', 'A4')
        test1('P5', 'P4')
        test1('A5', 'd4')
        test1('d6', 'A3')
        test1('m6', 'M3')
        test1('M6', 'm3')
        test1('A6', 'd3')
        test1('d7', 'A2')
        test1('m7', 'M2')
        test1('M7', 'm2')
        test1('A7', 'd2')
        test1('d8', 'A1')
        test1('P8', 'P1')
        test1('A8', 'd8') # exception to the rule

    def test_interval_complement_2(self):
        for n in Note.all(2, 3):
            n1 = n.to_octave(n.octave + 1)
            for i in Interval.all():
                if str(i) == 'A8': continue
                self.assertEqual(n + i + i.complement(), n1)
                self.assertEqual(n + i.complement() + i, n1)

    def test_interval_split(self):
        def test1(i, *args):
            self.assertEquals([str(i1) for i1 in Interval(i).split()], list(args))
        test1('M9', 'P8', 'M2')
        test1('m17', 'P8', 'P8', 'm3')
        test1('P29', 'P8', 'P8', 'P8', 'P8')


class TestsForChord(unittest.TestCase):
    def test_chord_creation(self):
        def test1(root, name, strchord):
            self.assertEqual(str(Chord(Note(root), name)), strchord)
        test1('A', 'M', 'Amaj')
        test1('B', 'm', 'Bmin')
        test1('C', 'dim', 'Cdim')
        test1('D', 'aug', 'Daug')
        test1('A#', 'M', 'A#maj')
        test1('Bb', 'M', 'Bbmaj')

        def test2(badname):
            self.assertRaises(Exception, Chord, badname)
        test2('A$')
        test2('H')

    def test_chord_recipes(self):
        def test1(root, name, intervals):
            r = Note(root)
            c = Chord(r, name)
            self.assertEqual(c.notes, [r + Interval(i) for i in intervals])
        test1('A', 'maj', ['P1', 'M3', 'P5'])
        test1('A', 'min', ['P1', 'm3', 'P5'])
        test1('A', 'dim', ['P1', 'm3', 'd5'])
        test1('A', 'aug', ['P1', 'M3', 'A5'])

    @unittest.skip('Note.__sub__ is broken')
    def test_recipes_intervals(self):
        for root in Note.all():
            for name, recipe in Chord.recipes.items():
                chord = Chord(root, name)
                notes = chord.notes
                derivedRecipe = [str(n - root) for n in notes]
                print(derivedRecipe)
                self.assertEqual(derivedRecipe, recipe)


class TestsForScale(unittest.TestCase):
    def test_note_scales(self):
        def test1(root, name, notes):
            self.assertEqual(list(map(str, Scale(Note(root), name).notes)), notes)
        test1('C', 'major',            ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        test1('C', 'natural_minor',    ['C', 'D', 'Eb','F', 'G', 'Ab','Bb'])
        test1('C', 'harmonic_minor',   ['C', 'D', 'Eb','F', 'G', 'Ab','B'])
        test1('C', 'melodic_minor',    ['C', 'D', 'Eb','F', 'G', 'A', 'B'])
        test1('C', 'dorian',           ['C', 'D', 'Eb','F', 'G', 'A', 'Bb'])
        test1('C', 'locrian',          ['C', 'Db','Eb','F', 'Gb','Ab','Bb'])
        test1('C', 'lydian',           ['C', 'D', 'E', 'F#','G', 'A', 'B'])
        test1('C', 'mixolydian',       ['C', 'D', 'E', 'F', 'G', 'A', 'Bb'])
        test1('C', 'phrygian',         ['C', 'Db','Eb','F', 'G', 'Ab','Bb'])
        test1('C', 'major_pentatonic', ['C', 'D', 'E', 'G', 'A'])
        test1('C', 'minor_pentatonic', ['C', 'Eb','F', 'G', 'Bb'])
        self.assertRaises(Exception, Scale, Note('C'), 'non-existent scale')

    def test_create_all_scales(self):
        for scale in Scale.all():
            pass

    def test_greek_modes_equivalence(self):
        cmaj = Scale('C', 'major')
        for i in range(7):
            s = Scale(cmaj[i], Scale.greek_modes[i + 1])
            for j in range(8):
                self.assertEqual(s[j], cmaj[i + j])


if __name__ == '__main__':
    unittest.main()
