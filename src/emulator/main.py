import sounddevice as sd
import numpy as np

class SongPlayer:
    def __init__(self, notes):
        self.notes = notes

    def play(self, duration):
        sample_rate = 44100

        total_samples = np.linspace(
            start=0,
            stop=duration,
            num= sample_rate * duration,
            endpoint=False
            )

        sound = np.zeros_like(total_samples)

        for frq in self.notes:
            sound += np.sin(2 * np.pi * frq * total_samples)
        
        sound = sound / len(sample_rate)

        sd.play(sound, sample_rate)
        sd.wait()
