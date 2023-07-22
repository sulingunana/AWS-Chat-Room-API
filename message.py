import websocket
import json
from base64 import b64encode, b64decode
import threading
import argparse
import sys
import msvcrt

# banner Ensar Gök ve Sülin Günana
banner = """
AWS Chat Client
Authors: Ensar Gök & Sülin Günana
"""

class ConnectionError(Exception):
    def __init__(self, message):
        print("[-] Bağlantı koptu, \n{}".format(message), file=sys.stderr)

class Terminal:
    def __init__(self, prompt = ">>> ") -> None:
        self.prompt = prompt
        self.yazi = ""

    def mesaj_yazdir(self, mesaj):
        sys.stdout.write("\r{}\r".format(" " * self.max_len))
        sys.stdout.write("{}\n".format(mesaj))
        sys.stdout.write("\r{}{}".format(self.prompt, self.yazi))
        sys.stdout.flush()

    def clear_line(self):
        sys.stdout.write("\r{}{}".format(self.prompt, self.yazi))
        sys.stdout.flush()

    def input_al(self) -> str:
        # sys.stdout.write(self.prompt)
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
                yazi = self.yazi
                self.yazi = ""
                return yazi

            # Normal character
            self.yazi += char

            sys.stdout.flush()


class Connection:
    def __init__(self, user_name, msg_to):
        self.MSG_LIST = ""
        self.name = user_name
        self.msg_to = msg_to
        try:
            print("[i] Bağlantı sağlanıyor.", end="")
            self.connection = websocket.create_connection(f"wss://28drcjvrtg.execute-api.eu-north-1.amazonaws.com/development?name={user_name}")
            self.connected = True
            print("\r[+] Bağlantı sağlandı.    ")
        except Exception as e:
            print("\r[-] Bağlantı sağlanamadı.    \nHata: {}".format(e), file=sys.stderr)
            self.connected = False
            exit(1)

    def recv_txt(self) -> str:
        try:
            recv = self.connection.recv()
            json_data = json.loads(recv)

            if json_data.get("status") == "success":
                # A message received
                msg_from = json_data["data"]["from"]
                msg_data = json_data["data"]["msg"]

                try:
                    msg = self.base64_decode(msg_data)
                except:
                    #print("\r[i] Mesaj base64 decode edilemedi. Mesaj: {}".format(msg_data), file=sys.stderr, end="\n>>> ")
                    msg = msg_data

                #print("\r{}: {}\n>>> ".format(msg_from, msg), end="")

                return "{}: {}".format(msg_from, msg)

                #self.MSG_LIST += "{}: {}\n".format(msg_from, msg)

            if json_data.get("status") == "failed":
                # Message sending failed
                print("\r[-] Mesaj gönderilemedi. Hata: {}\n>>> ".format(json_data["data"]), file=sys.stderr, end="")
        except ConnectionError:
            print("[-] Bağlantı koptu")
            return


    def base64_encode(self,txt):
        return b64encode(txt.encode()).decode()
    
    def base64_decode(self,txt):
        return b64decode(txt.encode()).decode()

    def write_to_client(self,txt):
        msg_data = self.base64_encode(txt)

        json_data = {"from": self.name, "to": self.msg_to, "message": msg_data, "action": "sendMessage"}
        data_to_send = json.dumps(json_data)
        self.connection.send(data_to_send)

        if self.MSG_LIST:
            #print(self.MSG_LIST, end="")
            self.MSG_LIST = ""

def listen_recv(connection: Connection, terminal: Terminal):
    while True:
        recv = connection.recv_txt()
        terminal.mesaj_yazdir(recv)


def main():
    parser = argparse.ArgumentParser(description='AWS Chat Client')
    parser.add_argument('-u', '--user', help='User name', required=True)
    parser.add_argument('-t', '--to', help='Message to', required=True)
    args = parser.parse_args()

    user = args.user
    msg_to = args.to

    print(banner)

    connection = Connection(user, msg_to)
    terminal = Terminal() 
    
    listen_thread = threading.Thread(target=listen_recv, args=(connection, terminal), daemon=True, name="ListenThread")
    listen_thread.start()


    while connection.connected:
        txt = terminal.input_al()
        terminal.mesaj_yazdir("{}: {}".format(user, txt))
        connection.write_to_client(txt)


if __name__ == "__main__":
    main()