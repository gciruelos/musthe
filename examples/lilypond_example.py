#!/usr/bin/env python   
# -*- coding: utf-8 -*-

from musthe import *


def lilypond_composer(bars, instrument='acoustic guitar (steel)', file_name='example.ly'):
    f = open(file_name, 'w')
    f.write('''\\score {
    \\new Voice \\relative c\' {
        \\set midiInstrument = #"'''+instrument+'"\n')
    for bar in bars:
        f.write('\t\t'+bar+'\n')
    f.write('''
    }
    \\midi{
        \\tempo 4 = 160
        \\context {
            \\Voice
            \\consists "Staff_performer"
        }
    }
    \\layout { }
}''')
    f.close()
    #timidity <input-file> -Ow -o <output-file>

def random_music():
    import random
    n = Note('Bb')
    pool = Scale(n, 'minor_pentatonic')

    for total_bars in range(4):
        bar = []
        notes_in_bar = 2**random.randrange(1, 3)

        index = 0
        for _ in range(notes_in_bar):
            note = pool[index].lilypond_notation()+str(notes_in_bar)

            '''
            difference = (bar[-1].octave)-(pool[index].octave)
            if difference == 1:
                note+=','
            elif difference == -1:
                note+='\''
            '''

            bar.append(note)

            change = int(random.gauss(0,2))
            while not 0<index+change<=len(pool):
                change = int(random.gauss(0,2))
            index+=change
        yield ' '.join(bar)

lilypond_composer(random_music())
