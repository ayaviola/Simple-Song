'''
Monophonic Song #1:
Personal transcription of Harry Dacre's 'Daisy Bell' 

In this example, I am using the emulator to play monophonic melodies instead
of polyphonic melodies. You can adjust this accordingly or inspire yourself off 
of this example.
'''

import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emulator.main import SongPlayer

NOTE_DURATION = 0.4

def frequency(note):
    ...