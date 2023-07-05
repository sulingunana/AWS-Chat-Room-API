import websocket
import json
from base64 import b64encode, b64decode

user_name = "terminal"

connection = websocket.create_connection(f"wss://28drcjvrtg.execute-api.eu-north-1.amazonaws.com/development?name={user_name}")

input_text = input(">>> ")
b64_text = b64encode(input_text.encode()).decode()
data = {"action": "sendMessage", "message": b64_text,"from": user_name, "to": "Ensar"}
data = json.dumps(data)

print("sending data", data)
try:
    connection.send(data)
except:
    connection.close()

print("receiving data")
try:
    gelen = connection.recv()
except:
    connection.close()

print("gelen", gelen)

data = json.loads(gelen)
b64_text = data["Message"]["data"]
print(b64decode(b64_text.encode()).decode())

connection.close()

def send_message():
    message = input(">>> ")
    data = {"action": "sendMessage", "message": message, "to" : "Sulin"}
    data = json.dumps(data)
    connection.send(data)
