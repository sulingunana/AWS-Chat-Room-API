import websocket
import json
from base64 import b64encode, b64decode
import sys
import threading

class Connection:
    def __init__(self, user_name, msg_to):
        self.MSG_LIST = ""
        self.name = user_name
        self.msg_to = msg_to
        try:
            self.connection = websocket.create_connection(f"wss://28drcjvrtg.execute-api.eu-north-1.amazonaws.com/development?name={user_name}")
        except:
            print("Hata")
            exit(1)
        listen_thread = threading.Thread(target=self.listen_recv)
        listen_thread.start()

    def listen_recv(self):
        while 1:
            recv = self.connection.recv()
            json_data = json.loads(recv)

            # if status == success -> message received
            if json_data["status"] != "success":
                exit(1)

            if json_data["message"] == "received":
                msg_from = json_data["data"]["from"]
                msg_data = json_data["data"]["msg"]
                msg = self.base64_decode(msg_data)

                self.MSG_LIST += "{}: {}\n".format(msg_from, msg)



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
        msg = input(prompt)
        self.write_to_client(msg)

def main():
    connection = Connection("Ensar", "Sulin")
    
    while True:
        connection.take_input()

if __name__ == "__main__":
    main()