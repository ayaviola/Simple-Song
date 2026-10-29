'''
PLEASE NOTE THAT THIS IS PURELY, AND I MEAN PURELY MY OWN PERSONAL EXAMPLE.
I WILL MAKE VARIOUS EXAMPLES OF VARIOUS SONGS, THIS IS ONE OF THE MANY EXAMPLES YOU COULD RE-USE (which I wouldn't mind!)
TINKER AND FIT IT TO YOUR STANDARDS, OR INSPIRE YOURSELF OFF OF AND LEARN HOW MY PROGRAM WORKS AND DIFFERENT CASES!!!!
'''

'''
For this example, I transcribed Kikuo - Twins at the Carousel !!
'''

import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emulator.main import SongPlayer

EIGHTH_NOTE_SECONDS = 60.0 / 67.0 / 3.0


def frequency(note):
    match = re.fullmatch(r'([A-G])([#b]?)(-?\d+)', note)
    if match is None:
        raise ValueError(note)
    letter, accidental, octave = match.groups()
    pitch = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}[letter]
    pitch += {'': 0, '#': 1, 'b': -1}[accidental]
    midi = 12 * (int(octave) + 1) + pitch
    return 440.0 * 2 ** ((midi - 69) / 12)


RIGHT_HAND = [
    [(3, 'B4 D#5 F#5'), (3, 'D#4 B4 D#5')],
    [(2.5, 'A#3 F#4 A#4'), (0.5, 'B3 G#4 B4'), (3, 'A#3 F#4 A#4')],
    [(0.5, notes) for n in notes [
        'B3 D#4', 'F#4', 'G#4', 'D#4 F#4', 'G#4', 'F#4 A#4',
        'A#4 C#5', 'G#4 B4', 'F#4', 'G#4 B4', 'A#4 C#5', 'B4 D#5',
    ]],
    [(6, 'A#4 C#5 E5')],
    [(3, 'G#4 C#5 E5'), (3, 'E4 A#4 C#5')],
    [(2, 'C#4 E4 C#5'), (1, 'E4 C#5 E5'), (3, 'C4 G#4 C5')],
    [(1, 'E4 C#5 E5'), (1, 'D#4 B4 D#5'), (1, 'C#4 A#4 C#5'),
     (2, 'B3 G#4 B4'), (1, 'A#3 F#4 A#4')],
    [(6, 'F#4 D#5 F#5')],
]


def accompaniment(bass1, chor1, bsas2, chord2):
    return [(1, n) for n in [bass1, chor1, chor1, bsas2, chord2, chord2]]


LEFT_HAND = [
    accompaniment('B2', 'D#3 F#3', 'F#2', 'D#3 F#3'),
    accompaniment('B2', 'D#3 F#3', 'F#2', 'D#3 F#3'),
    accompaniment('B1', 'B2 D#3', 'F#2', 'D#3 F#3'),
    accompaniment('C#2 E2', 'E3 G#3', 'C3', 'E3 G#3'),
    accompaniment('C#3', 'E3 G#3', 'G#2', 'E3 G#3'),
    accompaniment('C#3', 'E3 G#3', 'G#2', 'E3 G#3'),
    accompaniment('C#3', 'E3 G#3', 'F#2', 'D#3 F#3'),
    [(1.5, n) for n in ['B2 D#3 F#3', 'C3 D#3 F#3',
                        'C#3 D#3 F#3', 'F#2 D#3 F#3']],
]

RIGHT_LEVELS = [(0.75, 0.55), (0.55, 0.35), (0.35, 0.95), (0.95, 0.95),
                (0.75, 0.55), (0.55, 0.35), (0.35, 0.95), (0.95, 0.95)]
LEFT_LEVELS = [(0.35, 0.35), (0.35, 0.35), (0.35, 0.75), (0.75, 0.55),
               (0.55, 0.45), (0.45, 0.35), (0.35, 0.75), (0.75, 0.25)]


def build_timeline():
    events = []
    for hand, measures, levels in [
        ('right', RIGHT_HAND, RIGHT_LEVELS),
        ('left', LEFT_HAND, LEFT_LEVELS),    ]:
        for index, measure in enumerate(measures):
            if sum(duration for duration, _ in measure) != 6:
                raise ValueError(f'{hand} measure {index + 1} must total 6 eighths')
            offset = 0
            quiet, loud = levels[index]
            for duration, notes in measure:
                events.append({
                    'hand': hand,
                    'start_seconds': (index * 6 + offset) * EIGHTH_NOTE_SECONDS,
                    'duration_seconds': duration * EIGHTH_NOTE_SECONDS,
                    'frequencies': [frequency(note) for note in notes.split()],
                    'volume': quiet + (loud - quiet) * offset / 6,
                })
                offset += duration
    return sorted(events, key=lambda e: e['start_seconds'])


def play_song():
    player = SongPlayer([])
    player.play(
        duration=48 * EIGHTH_NOTE_SECONDS,
        events=build_timeline(),
    )

if __name__ == "__main__":
    play_song()

'''
Again. Purely an example. This isn't expected out of you, this is just
what you can make with the schematic in src > emulator > emulator.py
'''