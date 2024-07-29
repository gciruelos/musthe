#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Uses the Scale.harmonize_dict() method to generate a JSON file containing
a dictionary mapping notes to keys for every scale.
"""
import json
from musthe import Scale


all_the_chords = {}

for scale in Scale.all():
    scale_name = str(scale)
    all_the_chords[scale_name] = {}
    chords = scale.harmonize_dict()
    for k, v in chords.items():
        all_the_chords[scale_name][k] = [str(chord) for chord in v] if v is not None else v

with open("harmonized_scales_dict.json", 'w', encoding='utf-8') as fh:
    json.dump(all_the_chords, fh, indent=2)
