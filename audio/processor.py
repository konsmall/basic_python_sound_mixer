import sounddevice as sd

from config import settings
from audio.effects import *




reverb = Reverb(settings.SAMPLE_RATE)

def audio_callback(indata, outdata, frames, time, status):

    if status:
        print("Audio status:", status)

    audio = indata.copy()

    # Gain
    if settings.GAIN_ENABLE:
        audio = apply_gain(
            audio,
            settings.GAIN_MULTIPLIER
        )

    # Bit crusher
    if settings.BIT_CRUSHER_ENABLE:
        audio = bit_crush(audio)

    # Distorion
    if settings.DISTORTION_ENABLE:
        audio = distortion(audio, settings.DISTORTION_MULTIPLIER)

    # Reverb
    if settings.REVERB_ENABLE:
        audio = reverb.process(audio, settings.REVERB_MIX)

    # Noise Clip
    if settings.NOISE_CLIP_ENABLE:
        audio = noise_clip( audio, settings.NOISE_CLIP_THRESHOLD )

    outdata[:] = audio


def start_audio():

    print("Starting...")
    print(
        "Input :",
        sd.query_devices(settings.INPUT_DEVICE)["name"]
    )

    print(
        "Output:",
        sd.query_devices(settings.OUTPUT_DEVICE)["name"]
    )

    print()

    stream = sd.Stream(
        device=(
            settings.INPUT_DEVICE,
            settings.OUTPUT_DEVICE
        ),
        channels=settings.CHANNELS,
        dtype="float32",
        samplerate=settings.SAMPLE_RATE,
        callback=audio_callback,
        latency="low",
    )

    return stream
