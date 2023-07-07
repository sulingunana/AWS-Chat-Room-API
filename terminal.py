import shutil
import threading
from time import sleep
import sys

class Terminal():
    def __init__(self):
        self.last_height = 0

    def save_cursor_position(self):
        print("\033[s", end="")

    def restore_cursor_position(self):
        print("\033[u", end="")

    def move_cursor_to_bottom(self):
        _, rows = shutil.get_terminal_size()
        print("\033[{};{}H".format(rows, 0), end="")

    def print_on_top(self, text):
        print(f"Ensar: {text}")

    def sonradan_gelen_print(self, text):
        
        self.save_cursor_position()

        print(f"Sonradan gelen mesaj: {text}")
        
        self.restore_cursor_position()

        print("\033[1E",end="")  # Bir sonraki satıra geç
        

    def take_input(self):

        input_text = input(">>> ")
        sys.stdout.write("\033[F") # Şu anki satıra git
        sys.stdout.write("\033[K") # Satırı temizle

        return input_text

def arada_gelen_mesaj_prova():
    sleep(10)
    terminal.sonradan_gelen_print("Merhaba, ben arada gelen mesajım.")

if __name__ == "__main__":
    terminal = Terminal()

    threading.Thread(target=arada_gelen_mesaj_prova).start()


    for i in range(10):
        mesaj = terminal.take_input()
        terminal.print_on_top(mesaj)