#-Encoding: utf-8
import threading
import msvcrt
from time import sleep
import sys

def main():
    terminal = Terminal()


class Terminal:
    def __init__(self, prompt = ">>> ") -> None:
        self.prompt = prompt
        self.yazi = ""

    def mesaj_yazdir(self, mesaj):
        sys.stdout.write("\r{}\r".format(" " * self.max_len))
        sys.stdout.write("{}\n".format(mesaj))
        sys.stdout.flush()

    def clear_line(self):
        sys.stdout.write("\r{}{}".format(self.prompt, self.yazi))
        sys.stdout.flush()

    def input_al(self) -> str:
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

        self.max_len = len(self.prompt + self.yazi)

        while True:
            self.max_len = max(self.max_len, len(self.prompt + self.yazi))
            # clear the line to the end
            self.clear_line()

            sys.stdout.write("\r{}{}".format(self.prompt, self.yazi))

            char = msvcrt.getwch()

            if ord(char) == 8:
                # Backspace
                self.yazi = self.yazi[:-1]
                sys.stdout.write("\b \b")
                continue

            # esc 
            if ord(char) == 27:
                raise KeyboardInterrupt

            # CTRL + C
            if ord(char) == 3:
                raise KeyboardInterrupt
            
            # enter
            if ord(char) == 13:
                if self.yazi == "":
                    continue
                sys.stdout.write("\n")
                yazi = self.yazi
                self.yazi = ""
                return yazi

            # Normal character
            self.yazi += char

            sys.stdout.flush()


def main():
    terminal = Terminal()

    while True:
        txt = terminal.input_al()
        terminal.mesaj_yazdir("{}: {}".format("Ensar", txt))

if __name__ == "__main__":
    main()

