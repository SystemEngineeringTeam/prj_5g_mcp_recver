import os
import socket
import websocket
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

ENV_PORT = os.environ.get("PORT")
PORT = int(ENV_PORT) or 65500
ADDRESS = "127.0.0.1"
RECV_IDS = os.environ.get("RECV_IDS").split(",")

WS_API_URL = os.environ.get("WS_API_URL")


def on_message(ws, message):
    print(f"received: {message}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message, (ADDRESS, PORT))


def on_error(ws, error):
    print(f"error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"closed: [{close_status_code}] {close_msg}")


def on_open(ws):
    print(f"opened: {ws}")

def run(id):
    ws = websocket.WebSocketApp(
        urljoin(WS_API_URL, id),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    print(f"running: {id}")
    ws.run_forever()

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        for recv_id in RECV_IDS:
            executor.submit(run, recv_id)

        executor.shutdown(wait=True)
