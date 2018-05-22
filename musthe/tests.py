import unittest
from musthe import *


class TestsForLetter(unittest.TestCase):
    def test_letter_parsing(self):
        def test1(name):
            self.assertEqual(str(Letter(name)), name)
        for name in 'CDEFGAB':
            test1(name)

        def test2(badname):
            self.assertRaises(ValueError, Letter, badname)
        test2('C#')
        test2('Db')
        test2('H')
        test2('$')

    def test_letter_stuff(self):
        for i in 'DEGAB':
            self.assertTrue(Letter(i).has_flat())
        for i in 'CDFGA':
            self.assertTrue(Letter(i).has_sharp())

    def test_letter_arithmetic(self):
        def test1(letter, difference, result):
            norm = lambda n: (n + (1 if n < 1 else -1)) % 7 + 1
            letter = Letter(letter)
            result = Letter(result)
            self.assertEqual(letter + difference, result)
            self.assertEqual(result - difference, letter)
            self.assertEqual(norm(result - letter), norm(difference))
        test1('A', 2, 'B')
        test1('A', 3, 'C')
        test1('A', 5, 'E')
        test1('G', 11, 'C')
        test1('D', 1, 'D')
        test1('D', -2, 'C')

        self.assertRaises(ValueError, lambda: Letter('D') + 0)

        self.assertRaises(TypeError, lambda: Letter('E') + object())
        self.assertRaises(TypeError, lambda: Letter('F') - object())

    def test_letter_repr(self):
        self.assertEqual(repr(Letter('C')), 'Letter({!r})'.format('C'))

        def test2(letter1, letter2, difference):
            self.assertEqual(Letter(letter1) - Letter(letter2), difference)
        test2('D', 'C', 2)
        test2('C', 'B', -7)

        def test3(letter1, difference, letter2):
            self.assertEqual(Letter(letter1) - difference, Letter(letter2))
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
            self.assertEqual(Note(note).midi_note(), midi)
        test1('C4', 60)
        test1('D5', 74)

    def test_note_add(self):
        def test1(note, interval, result):
            note = Note(note)
            interval = Interval(interval)
            result = Note(result)
            self.assertEqual(note + interval, result)
            self.assertEqual(result - interval, note)
            self.assertEqual(result - note, interval)
        test1('A4', 'd5', 'Eb5')
        test1('A4', 'P1', 'A4')
        test1('G##4', 'm3', 'B#4')
        test1('F3', 'P5', 'C4')
        test1('B#4', 'd2', 'C5')
        test1('C4', 'd1', 'Cb4')
        test1('B4', 'd1', 'Bb4')
        test1('C#4', 'd1', 'C4')
        # compound intervals:
        test1('C4', 'M10', 'E5')
        test1('Cb4', 'A10', 'E5')
        test1('Cb4', 'm10', 'Ebb5')
        test1('B3', 'm10', 'D5')
        test1('B3', 'M17', 'D#6')

        self.assertRaises(TypeError, lambda: Note('C') + object())
        self.assertRaises(TypeError, lambda: Note('C') + 'sdfgh#$%')

    def test_note_sub(self):
        def test1(note1, note2, result):
            self.assertEqual(Note(note1) - Note(note2), Interval(result))
        test1('E', 'C', 'M3')
        test1('G', 'C', 'P5')
        test1('C#', 'C', 'A1')
        test1('Cb', 'C', 'd1')

        self.assertRaises(ArithmeticError, lambda: Note('C4') - Note('C5'))

        self.assertRaises(TypeError, lambda: Note('C') - object())
        self.assertRaises(TypeError, lambda: Note('C') - 'sdfgh#$%')

        # remove this test if doubly augmented/diminished intervals are introduced:
        self.assertRaises(ValueError, lambda: Note('A#4') - Note('Gb4'))

    def test_note_freq(self):
        def test1(note, freq):
            self.assertAlmostEqual(Note(note).frequency(), freq, 1)
        test1('A4', 440.0)
        test1('A5', 880.0)
        test1('C5', 523.3)

    def test_note_lilypond(self):
        def test1(n, l):
            self.assertEqual(Note(n).lilypond_notation(), l)
        test1('C', 'c')
        test1('C#', 'cis')
        test1('Cb', 'ces')

    def test_note_repr(self):
        self.assertEqual(repr(Note('C#4')), 'Note({!r})'.format('C#4'))


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
        test1('A8', 'd1')

        self.assertRaises(ValueError, lambda: Interval('M10').complement())

    def test_interval_complement_2(self):
        for n in Note.all(2, 3):
            n1 = n.to_octave(n.octave + 1)
            for i in Interval.all():
                self.assertEqual(n + i + i.complement(), n1)
                self.assertEqual(n + i.complement() + i, n1)

    def test_interval_split(self):
        def test1(i, *args):
            self.assertEqual([str(i1) for i1 in Interval(i).split()], list(args))
        test1('M9', 'P8', 'M2')
        test1('m17', 'P8', 'P8', 'm3')
        test1('P29', 'P8', 'P8', 'P8', 'P8')

    def test_interval_repr(self):
        self.assertEqual(repr(Interval('P4')), 'Interval({!r})'.format('P4'))


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

        def test3(root, badtype):
            self.assertRaises(ValueError, Chord, Note(root), badtype)
        test3('C', 'nice')
        test3('C', '$')
        test3('C', 'diminished')

    def test_chord_parsing(self):
        def test1(name, root, chord_type):
            self.assertEqual(Chord(name), Chord(Note(root), chord_type))
        test1('CM', 'C', 'maj')
        test1('Cmaj', 'C', 'maj')
        test1('Cmaj', 'C', 'M')
        test1('Cmaj7', 'C', 'M7')
        test1('D#aug7', 'D#', 'aug7')
        test1('Cbdim', 'Cb', 'dim')

    def test_chord_gen(self):
        roots = (Note('C'), Note('D'))
        list(Chord.all())
        list(Chord.all(root=tuple(roots)))
        list(Chord.all(root=list(roots)))
        #list(Chord.all(root=set(roots))) # Note is not hashable
        list(Chord.all(root=roots[0]))

        self.assertRaises(TypeError, lambda: list(Chord.all(root='vdfjy#$')))

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

    def test_chord_repr(self):
        self.assertEqual(repr(Chord(Note('C'), 'dim7')), 'Chord({!r}, {!r})'.format(Note('C'), 'dim7'))

    def test_chord_equality(self):
        self.assertNotEqual(Chord('Cdim'), Chord('Cdim7'))


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

    def test_scale_parsing(self):
        self.assertRaises(Exception, Scale, Note('C'), 'non-existent scale')
        self.assertRaises(TypeError, Scale, object(), 'major')

    def test_scale_getitem(self):
        s = Scale('C', 'harmonic_minor')
        self.assertRaises(IndexError, lambda: s[-1357788])
        self.assertRaises(TypeError, lambda: s[object()])
        self.assertEqual(s[10:15], [Note(x) for x in ('F5', 'G5', 'Ab5', 'B5', 'C6')])

    def test_create_all_scales(self):
        for scale in Scale.all():
            pass

    def test_greek_modes_equivalence(self):
        cmaj = Scale('C', 'major')
        for i in range(7):
            s = Scale(cmaj[i], Scale.greek_modes[i + 1])
            for j in range(8):
                self.assertEqual(s[j], cmaj[i + j])

    def test_scale_containment(self):
        scale = Scale('C', 'major')

        notes = (Note('E'), Note('F'))
        notes2 = (Note('Eb'), Note('F#'))
        self.assertTrue(notes[0] in scale)
        self.assertFalse(notes2[0] in scale)
        self.assertTrue(notes in scale)
        self.assertTrue(list(notes) in scale)
        self.assertFalse(notes2 in scale)

        chords = (Chord('Fmaj'), Chord('Emin'))
        chords2 = (Chord('Edim7'), Chord('Fdom7'))
        self.assertTrue(chords[0] in scale)
        self.assertFalse(chords2[0] in scale)
        self.assertTrue(chords in scale)
        self.assertFalse(chords2 in scale)

        self.assertFalse(object() in scale)

    def test_scale_repr(self):
        scale = Scale('C', 'major')
        self.assertEqual(str(scale), 'C major')
        self.assertEqual(repr(scale), 'Scale({!r}, {!r})'.format(scale.root, scale.name))


if __name__ == '__main__':
    unittest.main()
