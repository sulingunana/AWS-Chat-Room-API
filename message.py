import websocket
import json
from base64 import b64encode, b64decode
import threading
import argparse
import sys

# banner Ensar Gök ve Sülin Günana
banner = """
AWS Chat Client
Authors: Ensar Gök & Sülin Günana
"""

class ConnectionError(Exception):
    def __init__(self, message):
        print("[-] Bağlantı koptu, \n{}".format(message), file=sys.stderr)


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
        self.listen_thread = threading.Thread(target=self.listen_recv, daemon=True, name="ListenThread")
        self.listen_thread.start()
        self.listen_thread.join(1)

    def listen_recv(self):
        try:
            while 1:
                recv = self.connection.recv()
                json_data = json.loads(recv)


                if json_data.get("status") != "success":
                    print("\n[-] Bir hata oluştu: {}".format(json_data.get("message")))
                    self.connected = False
                    raise ConnectionError("[-] Bir hata oluştu: {}".format(json_data.get("message")))

                if json_data.get("message") == "received":
                    msg_from = json_data["data"]["from"]
                    msg_data = json_data["data"]["msg"]
                    msg = self.base64_decode(msg_data)

                    print("\r{}: {}\n>>> ".format(msg_from, msg), end="")

                    #self.MSG_LIST += "{}: {}\n".format(msg_from, msg)
        except ConnectionError:
            print("[-] Bağlantı koptu.3")
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
            print(self.MSG_LIST, end="")
            self.MSG_LIST = ""

    def take_input(self, prompt = ">>> "):
        try:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            msg = sys.stdin.readline().strip()
        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)
        except ConnectionError:
            print("\nExiting2")
            exit(0)
        self.write_to_client(msg)

def main():
    parser = argparse.ArgumentParser(description='AWS Chat Client')
    parser.add_argument('-u', '--user', help='User name', required=True)
    parser.add_argument('-t', '--to', help='Message to', required=True)
    args = parser.parse_args()

    user = args.user
    msg_to = args.to

    print(banner)

    connection = Connection(user, msg_to)
    
    while connection.connected:
        connection.take_input()

if __name__ == "__main__":
    main()