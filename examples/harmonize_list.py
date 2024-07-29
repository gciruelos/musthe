#!/usr/bin/env python   
# -*- coding: utf-8 -*-
"""Uses the Scale.harmonize() method to generate a JSON file containing
lists of chords for every note of every scale.
"""
import json
from musthe import Scale

all_the_chords = {}

for scale in Scale.all():
    scale_name = str(scale)
    all_the_chords[scale_name] = []
    chords = scale.harmonize()
    for i, n in enumerate(scale.notes):
        all_the_chords[scale_name].append([str(chord) for chord in chords[i]] if chords[i] is not None else None)
   
    
with open('harmonized_scales_list.json', 'w', encoding='utf-8') as fh:
    json.dump(all_the_chords, fh, indent=2)
