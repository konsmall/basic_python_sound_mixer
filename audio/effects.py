import numpy as np

from config import settings


def apply_gain(audio, multiplier):
    """Increase or decrease the audio amplitude."""
    audio = audio * multiplier
    return np.clip(audio, -1.0, 1.0)


def bit_crush(audio):
    """Apply bit-depth and sample-rate reduction."""

    levels = 2 ** settings.BIT_CRUSHER_BIT_DEPTH

    crushed = np.round(audio * levels) / levels

    # Sample-rate reduction
    crushed = crushed.copy()

    for i in range(0, len(crushed), settings.BIT_CRUSHER_DOWNSAMPLE):
        end = min(
            i + settings.BIT_CRUSHER_DOWNSAMPLE,
            len(crushed)
        )

        crushed[i:end] = crushed[i]

    return crushed



def distortion(audio, drive):

    audio = audio * drive

    audio = np.sin(audio * np.pi)

    return audio





class Reverb:

    def __init__(self, sample_rate=48000):

        self.delays = [
            int(sample_rate * 0.030),
            int(sample_rate * 0.045),
            int(sample_rate * 0.070),
        ]

        self.decays = [0.45, 0.30, 0.20]

        self.buffers = [
            np.zeros(delay, dtype=np.float32)
            for delay in self.delays
        ]

        self.positions = [0, 0, 0]

    def process(self, audio, mix=0.3):

        # Convert (frames, 1) -> (frames,)
        audio = audio[:, 0]

        output = audio.copy()

        for i in range(len(audio)):

            wet = 0.0

            for n in range(len(self.delays)):

                pos = self.positions[n]

                delayed = self.buffers[n][pos]

                wet += delayed * self.decays[n]

                self.buffers[n][pos] = audio[i]

                self.positions[n] += 1

                if self.positions[n] >= self.delays[n]:
                    self.positions[n] = 0

            output[i] = (
                audio[i] * (1.0 - mix)
                + wet * mix
            )

        # Convert (frames,) -> (frames, 1)
        return output.reshape(-1, 1)



def noise_clip(audio, threshold):
    return np.where(
        np.abs(audio) < threshold,
        0.0,
        audio
    )
