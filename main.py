from audio.processor import start_audio
from commands.handler import handle_command


def main():

    print("Voice Filter")
    print("Type 'exit' to quit.")
    print()

    with start_audio():

        while True:

            command = input("> ")

            if not handle_command(command):
                break


if __name__ == "__main__":
    main()
