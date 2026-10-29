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
            num= int(sample_rate * duration),
            endpoint=False
            )

        sound = np.zeros_like(total_samples)

        for frq in self.notes:
            sound += np.sin(2 * np.pi * frq * total_samples)
        
        if len(self.notes) > 0:
            sound /= len(self.notes)

        sd.play(sound, sample_rate)
        sd.wait()
