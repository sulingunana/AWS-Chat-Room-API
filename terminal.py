import shutil
import threading
from time import sleep

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
        for i in range(self.last_height):
            print()
        print(text,end="")
        self.last_height += 1
        self.move_cursor_to_bottom()

    def take_input(self):
        self.save_cursor_position()

        # when client press enter, >>> will be deleted
        input_text = input(">>> ")
        
        self.restore_cursor_position()        
        return input_text

def listen_thread(terminal):
    for i in range(10):
        sleep(3)
        terminal.restore_cursor_position()
        print("hello",end="")

if __name__ == "__main__":
    terminal = Terminal()

    listen_thread = threading.Thread(target=listen_thread, args=(terminal,))
    listen_thread.start()

    for i in range(10):
        input_text = terminal.take_input()
        print(input_text)

    listen_thread.kill()