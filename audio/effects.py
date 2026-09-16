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

    def __init__(self, delays, decays, sample_rate):
        self.delays = [int( sample_rate * delay) for delay in delays]

        self.decays = decays

        self.buffers = [
            np.zeros(delay, dtype=np.float32)
            for delay in self.delays
        ]

        self.positions = [int( 0 * delay) for delay in delays]

    def reinitialise(self, delays, decays, sample_rate):
        self.delays = [int( sample_rate * delay) for delay in delays]

        self.decays = decays

        self.buffers = [
            np.zeros(delay, dtype=np.float32)
            for delay in self.delays
        ]

        self.positions = [int( 0 * delay) for delay in delays]

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
    return np.where( np.abs(audio) < threshold, 0.0, audio )

def noise_gate(audio, threshold):
    level = np.sqrt(np.mean(audio ** 2))

    if level < threshold:
        return np.zeros_like(audio)

    return audio



# --------------------------------------------------
# FFT
# --------------------------------------------------

def fft(audio):
    return np.fft.rfft(audio, axis=0)


def get_frequencies(audio):
    return np.fft.rfftfreq(
        len(audio),
        1 / settings.SAMPLE_RATE
    )


def inverse_fft(spectrum, length):
    return np.fft.irfft( spectrum, n=length, axis=0)


# --------------------------------------------------
# Frequency filters
# --------------------------------------------------

def lowpass(spectrum, frequencies, cutoff):
    spectrum[frequencies > cutoff] = 0

    return spectrum


def highpass(spectrum, frequencies, cutoff):
    spectrum[frequencies < cutoff] = 0

    return spectrum

def lowpass_linear(spectrum, frequencies, cutoff, transition):
    f = frequencies


    gain = np.ones_like(f)

    start = cutoff - transition
    end = cutoff

    # Above cutoff -> completely remove
    gain[f >= end] = 0.0

    # Transition region -> linearly fade out
    mask = (f > start) & (f < end)

    gain[mask] = (end - f[mask]) / transition
    # gain = gain[:, np.newaxis]

    for i in range(0, len(spectrum)):
        spectrum[i][0] = spectrum[i][0] * gain[i]

    return spectrum

def highpass_linear(spectrum, frequencies, cutoff, transition):
    f = frequencies

    gain = np.ones_like(f)

    start = cutoff
    end = cutoff + transition

    # Below cutoff -> completely remove
    gain[f <= start] = 0.0

    # Transition region -> linearly fade in
    mask = (f > start) & (f < end)

    gain[mask] = (f[mask] - start) / transition
    gain = gain[:, np.newaxis]

    return spectrum * gain


def boost_frequency(
    spectrum,
    frequencies,
    frequency,
    width,
    amount
):
    mask = np.abs(frequencies - frequency) < width

    spectrum[mask] *= amount

    return spectrum



# def lowpass_linear(spectrum, frequencies, cutoff, transition):

#     f = np.abs(frequencies)

#     gain = np.ones_like(f)

#     # Start of roll-off
#     start = cutoff

#     # End of roll-off
#     end = cutoff + transition

#     # Linear transition
#     mask = (f > start) & (f < end)

#     gain[f >= end] = 0.0

#     gain[mask] = 1.0 - (
#         (f[mask] - start) /
#         (end - start)
#     )

#     return spectrum * gain