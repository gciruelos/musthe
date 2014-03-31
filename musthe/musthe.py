'''
Copyright (c) 2014 Gonzalo Ciruelos <gonzalo.ciruelos@gmail.com>
'''



import re


def scale(note, scale_name):
	if scale_name=='major':
		return [note, note+Interval('M2'), note+Interval('M3'), 
				note+Interval('P4'), note+Interval('P5'),
				note+Interval('M6'), note+Interval('M7'), 
				note+Interval('P8')]
	elif scale_name=='natural_minor':
		return [note, note+Interval('M2'), note+Interval('m3'), 
				note+Interval('P4'), note+Interval('P5'),
				note+Interval('m6'), note+Interval('m7'), 
				note+Interval('P8')]
	elif scale_name=='harmonic_minor':
		return [note, note+Interval('M2'), note+Interval('m3'), 
				note+Interval('P4'), note+Interval('P5'),
				note+Interval('m6'), note+Interval('M7'), 
				note+Interval('P8')]
	elif scale_name=='melodic_minor':
		return [note, note+Interval('M2'), note+Interval('m3'), 
				note+Interval('P4'), note+Interval('P5'),
				note+Interval('M6'), note+Interval('M7'), 
				note+Interval('P8')]
	elif scale_name=='minor_pentatonic':
		return [note, note+Interval('m3'), note+Interval('P4'),
				note+Interval('P5'), note+Interval('m7'), 
				note+Interval('P8')]
	else:
		raise Exception('No scale named '+scale_name) 



class Note():
	'''
	The note class.
	
	The notes are to be parsed in th following way:
	* the letter name, 
	* accidentals (up to 3), 
	* octave (default is 4).
	
	For example, 'Ab', 'G9', 'B##7' are all valid notes. '#', 'A9b', 
	'Dbbbb' are not.
	'''
	def __init__(self, note):
		note_pattern = re.compile(r'^[A-G]([b#])?\1{0,2}?\d?$') #raw because of '\'
		if note_pattern.search(note) == None:
			raise Exception('Could not parse the note: '+note)
		
		self.tone = note[0]
		self.accidental = re.findall('[b#]{1,3}', note)
		self.octave = re.findall('[0-9]', note)
		
		
		if self.accidental == []:
			self.accidental = ''
		else:
			self.accidental = self.accidental[0]
			
		if self.octave == []:
			self.octave = 4
		else:
			self.octave = int(self.octave[0])
		
		self.note_id = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}[self.tone]
		for change in self.accidental:
			if change == '#': self.note_id += 1
			elif change == 'b': self.note_id -= 1
		self.note_id %= 12
			
			
	def __add__(self, interval):
		if not isinstance(interval, Interval):
			raise Exception('Cannot add '+type(interval)+' to a note.')
		
		# * _old_note is the index in the list of the old note tone.
		# * new_note_tone is calculated adding the interval_number-1 because
		# you have start counting in the current tone. e.g. the fifth of
		# E is: (E F G A) B.
		_old_tone = 'CDEFGABCDEFGABCDEFGAB'.index(self.tone)
		new_note_tone = 'CDEFGABCDEFGABCDEFGAB'[_old_tone+interval.number-1]
		
		# %12 because it wraps in B->C and starts over.
		new_note_id = (self.note_id+interval.semitones)%12
		
		# First calculates the note, and then the difference from the note
		# without accidentals, then adds proper accidentals. 
		difference = new_note_id - {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}[new_note_tone]
		# In some cases, like G##+m3, difference is -11, and it should be
		# 1, so this corrects the error.
		if abs(difference)>3:
			difference = difference + 12
			
		if difference<0: accidental = 'b'*abs(difference)
		elif difference>0: accidental = '#'*abs(difference)
		else: accidental = ''
		
		
		# it calculates how many times it wrapped around B->C and adds.
		new_note_octave = (self.note_id+interval.semitones)//12+self.octave
		# corrects cases like B#, B##, B### and A###.
		# http://en.wikipedia.org/wiki/Scientific_pitch_notation#C-flat_and_B-sharp_problems
		if new_note_tone+accidental in ['B#', 'B##', 'B###', 'A###']:
			new_note_octave -= 1
		
		return Note(new_note_tone+accidental+str(new_note_octave))
		

	def frequency(self):
		'''
		Returns frequency in Hz. It uses the method given in
		http://en.wikipedia.org/wiki/Note#Note_frequency_.28hertz.29
		'''
		pass
	
	def lilypond_notation(self):
		return str(self).replace('b', 'is').replace('#','es').lower()
	
	def scientific_notation(self):
		return str(self)+str(self.octave)
	
	def __repr__(self):
		return "Note(\"%s\")" % self.scientific_notation()
			
	def __str__(self):
		return self.tone+self.accidental


class Interval():
	'''
	The interval class.
	
	The notes are to be parsed in th following way:
	* the quality, (m, M, p, A, d)
	* the number. (1 to 8) [Compound intervals will be supported]
	
	For example, 'd8', 'P1', 'A5' are valid intervals. 'P3', '5' are not.
	'''
	def __init__(self, interval):
		try:
			self.semitones = {'P1': 0, 'A1':1, 'd2':0, 'm2':1, 'M2':2, 'A2':3,
							  'd3':3, 'm3':3, 'M3':4, 'A3':5, 'd4':4, 'P4':5,
							  'A4':6, 'd5':6, 'P5':7, 'A5':8, 'd6':7, 'm6':8,
							  'M6':9, 'A6':10,'d7':9, 'm7':10, 'M7':11, 'A7':12,
							  'd8':11, 'P8':12}[interval]
		except:
			raise Exception('Could not parse the interval.')
		self.number = int(interval[1])
		


if __name__ == '__main__':
	pass
	
