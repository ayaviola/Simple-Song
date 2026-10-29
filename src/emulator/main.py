import sounddevice as sd
import numpy as np

class SongPlayer:
    def __init__(self, notes):
        self.notes = notes

    def play(self, duration, events=None):
        sample_rate = 44100
        sound = np.zeros(round(sample_rate * duration))

        if events is None:
            events = [{
                "start_seconds": 0,
                "duration_seconds": duration,
                "frequencies": self.notes,
                "volume": 1,
            }]

        for event in events:
            start = round(event["start_seconds"] * sample_rate)
            end = round(
                (event["start_seconds"] + event["duration_seconds"])
                * sample_rate
            )
            end = min(end, len(sound))

            if end <= start:
                continue

            time = np.arange(end - start) / sample_rate

            fade_in = np.minimum(time / 0.008, 1)
            fade_out = np.minimum((time[-1] - time) / 0.025, 1)
            envelope = fade_in * fade_out * np.exp(-0.65 * time)

            for frequency in event["frequencies"]:
                phase = 2 * np.pi * frequency * time
                tone = (
                    np.sin(phase)
                    + 0.20 * np.sin(2 * phase)
                    + 0.07 * np.sin(3 * phase)
                )
                sound[start:end] += (
                    tone * envelope * event.get("volume", 1)
                )

        peak = np.max(np.abs(sound)) if sound.size else 0
        if peak:
            sound *= 0.9 / peak

        sd.play(sound, sample_rate)
        sd.wait()