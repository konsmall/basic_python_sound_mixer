from audio.effects import *
from audio.processor import reverb

# Example Filters: Frequency related filters are always after time domain
# filters = [
#     # Time-domain
#     (lambda audio: apply_gain(audio, settings.GAIN_MULTIPLIER), "time"),
#     (lambda audio: bit_crush(audio), "time"),
#     (lambda audio: distortion(audio, settings.DISTORTION_MULTIPLIER), "time"),
#     (lambda audio: reverb.process(audio, settings.REVERB_MIX), "time"),
#     (lambda audio: noise_clip(audio, settings.NOISE_CLIP_THRESHOLD), "time"),

#     # Frequency-domain
#     (lambda s, f: lowpass(s, f, 5000), "frequency"),
#     (lambda s, f: boost_frequency(s, f, 1000, 200, 2), "frequency"),
#     (lambda s, f: boost_frequency(s, f, 3000, 300, 1.5), "frequency"),
# ]


filters = [
    # Time-domain
    (lambda audio: noise_gate(audio, settings.NOISE_CLIP_THRESHOLD), "time"),
    (lambda audio: apply_gain(audio, 4), "time"),
    # (lambda audio: reverb.process(audio, 0.3), "time"),
    # (lambda audio: bit_crush(audio), "time"),
    # (lambda audio: noise_clip(audio, settings.NOISE_CLIP_THRESHOLD), "time"),
    # (lambda audio: noise_gate(audio, settings.NOISE_CLIP_THRESHOLD), "time"),

    # Frequency-domain
    # (lambda s, f: lowpass(s, f, 10000), "frequency"),
    # (lambda s, f: highpass(s, f, 1000), "frequency"),
    # (lambda s, f: lowpass_linear(s, f, 6000, 2000), "frequency"),
    # (lambda s, f: highpass_linear(s, f, 3000, 500), "frequency"),
    # (lambda s, f: boost_frequency(s, f, 3500, 200, 0), "frequency"),
]