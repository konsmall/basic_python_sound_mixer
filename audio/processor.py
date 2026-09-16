import sounddevice as sd

from config import settings
from audio.effects import *


# reverb = Reverb(settings.SAMPLE_RATE)
reverb = Reverb(settings.REVERB_DELAYS, settings.REVERB_DECAYS, settings.SAMPLE_RATE)
from config import filter_list



def audio_callback(indata, outdata, frames, time, status):

    if status:
        print("Audio status:", status)

    audio = indata.copy()

    # -------------------------
    # Time-domain filters
    # -------------------------
    for filter_function, domain in filter_list.filters:
        if domain == "time":
            audio = filter_function(audio)


    # -------------------------
    # Frequency-domain filters
    # -------------------------
    spectrum = fft(audio)
    frequencies = get_frequencies(audio)


    for filter_function, domain in filter_list.filters:
        if domain == "frequency":
            spectrum = filter_function(
                spectrum,
                frequencies
            )


    # -------------------------
    # Back to time domain
    # -------------------------
    audio = inverse_fft(
        spectrum,
        len(audio)
    )


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
