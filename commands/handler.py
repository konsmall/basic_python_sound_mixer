import importlib
from config import settings, filter_list

from audio.processor import reverb

def handle_command(command):

    parts = command.strip().split()

    if not parts:
        return True

    command_name = parts[0]

    # EXIT
    if command_name == "exit":
        return False

    # SHOW DEVICES
    elif command_name == "SHOW_DEVICES":
        import sounddevice as sd
        print(sd.query_devices())

    # ~~~~~~~~~~~~~~~~~~~~~~~ GAIN ~~~~~~~~~~~~~~~~~~~~~~~
    elif command_name == "GAIN_ENABLE":

        try:
            value = int(parts[1])

            if value < 0 or value > 1:
                print("Please enter 0 or 1.")
                return True

            settings.GAIN_ENABLE = value

            print(
                "Gain Enable:",
                settings.GAIN_ENABLE
            )

        except (ValueError, IndexError):
            print("Usage: GAIN_ENABLE 0/1")

    elif command_name == "GAIN_MULTIPLIER":

        try:
            value = float(parts[1])

            if value < 0.0 or value > 100.0:
                print("Please enter a value between 0 and 100.")
                return True

            settings.GAIN_MULTIPLIER = value

            print(
                "Gain Multiplier:",
                settings.GAIN_MULTIPLIER
            )

        except (ValueError, IndexError):
            print("Usage: GAIN_MULTIPLIER 2.0")

    # ~~~~~~~~~~~~~~~~~~~~~~~ BIT CRUSHER ~~~~~~~~~~~~~~~~~~~~~~~
    elif command_name == "BIT_CRUSHER_ENABLE":
        try:
            value = int(parts[1])

            if value not in (0, 1):
                print("Please enter 0 or 1.")
                return True

            settings.BIT_CRUSHER_ENABLE = value

            print(
                "Bit Crusher:",
                settings.BIT_CRUSHER_ENABLE
            )

        except (ValueError, IndexError):
            print("Usage: BIT_CRUSHER_ENABLE 0/1")

    elif command_name == "BIT_CRUSHER_BIT_DEPTH":
        try:
            value = int(parts[1])

            if value < 1 or value > 64:
                print("Please enter a value between 1 and 64.")
                return True

            settings.BIT_CRUSHER_BIT_DEPTH = value

            print(
                "Bit Depth:",
                settings.BIT_CRUSHER_BIT_DEPTH
            )

        except (ValueError, IndexError):
            print("Usage: BIT_CRUSHER_BIT_DEPTH 4")

    elif command_name == "BIT_CRUSHER_DOWNSAMPLE":
        try:
            value = int(parts[1])

            if value < 1 or value > 64:
                print("Please enter a value between 1 and 64.")
                return True

            settings.BIT_CRUSHER_DOWNSAMPLE = value

            print( "Downsampling:", settings.BIT_CRUSHER_DOWNSAMPLE )

        except (ValueError, IndexError):
            print("Usage: BIT_CRUSHER_DOWNSAMPLE 8")

    # ~~~~~~~~~~~~~~~~~~~~~~~ DISTORTION ~~~~~~~~~~~~~~~~~~~~~~~
    elif command_name == "DISTORTION_ENABLE":
        try:
            value = int(parts[1])

            if value not in (0, 1):
                print("Please enter 0 or 1.")
                return True

            settings.DISTORTION_ENABLE = value

            print( "DISTORTION_ENABLE:", settings.DISTORTION_ENABLE )

        except (ValueError, IndexError):
            print("Usage: DISTORTION_ENABLE 0/1")
    elif command_name == "DISTORTION_MULTIPLIER":
        try:
            value = int(parts[1])

            if value < 0.0 or value > 100.0:
                print("Please enter a value between 0 and 100.")
                return True

            settings.DISTORTION_MULTIPLIER = value

            print( "Distortion Multiplier:", settings.DISTORTION_MULTIPLIER )

        except (ValueError, IndexError):
            print("Usage: DISTORTION_MULTIPLIER 2.4")

    # ~~~~~~~~~~~~~~~~~~~~~~~ REVERB ~~~~~~~~~~~~~~~~~~~~~~~
    elif parts[0] == "REVERB_ENABLE":
        try:
            value = int(parts[1])

            if value not in (0, 1):
                print("Please enter 0 or 1.")
                return True

            settings.REVERB_ENABLE = value

            print( "Reverb:", settings.REVERB_ENABLE )

        except (ValueError, IndexError):
            print("Usage: REVERB_ENABLE 0/1")
    elif parts[0] == "REVERB_MIX":

        try:
            value = float(parts[1])

            if value < 0 or value > 1:
                print("Mix must be between 0 and 1.")
                return True

            settings.REVERB_MIX = value

            print( "Reverb mix:", settings.REVERB_MIX )

        except (ValueError, IndexError):
            print("Usage: REVERB_MIX 0.3")


    # ~~~~~~~~~~~~~~~~~~~~~~~ Noise Clip ~~~~~~~~~~~~~~~~~~~~~~~
    elif parts[0] == "NOISE_CLIP_ENABLE":
        try:
            value = int(parts[1])

            if value not in (0, 1):
                print("Please enter 0 or 1.")
                return True

            settings.NOISE_CLIP_ENABLE = value

            print( "Noise CLip:", settings.NOISE_CLIP_ENABLE )

        except (ValueError, IndexError):
            print("Usage: NOISE_CLIP_ENABLE 0/1")
    elif parts[0] == "NOISE_CLIP_THRESHOLD":

        try:
            value = float(parts[1])

            if value < 0 or value > 1:
                print("Mix must be between 0 and 1.")
                return True

            settings.NOISE_CLIP_THRESHOLD = value

            print( "Reverb mix:", settings.NOISE_CLIP_THRESHOLD )

        except (ValueError, IndexError):
            print("Usage: NOISE_CLIP_THRESHOLD 0.2")

    elif command_name == "reload":
        importlib.reload(settings)
        importlib.reload(filter_list)
        reverb.reinitialise( settings.REVERB_DELAYS, settings.REVERB_DECAYS, settings.SAMPLE_RATE )
        # from config.filter_list import filters
        print("Settings reloaded.")


    else:
        print("Unknown command:", command_name)

    return True
