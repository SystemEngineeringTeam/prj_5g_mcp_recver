import os
import socket
from urllib.parse import urljoin
from websocket import WebSocket, WebSocketApp
from concurrent.futures import ThreadPoolExecutor

PORT = int(os.environ.get("PORT") or 65500)
ADDRESS = "127.0.0.1"
RECV_IDS = os.environ.get("RECV_IDS").split(",")

WS_API_URL = os.environ.get("WS_API_URL")


def on_message(ws, message: bytes | str):
    recv_id = ws.recv_id
    str_message = message if type(message) == str else message.decode()
    print(f"received[{recv_id}]: {str_message}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(str_message.encode(), (ADDRESS, PORT))


def on_error(ws, error):
    print(f"error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"closed: [{close_status_code}] {close_msg}")


def on_open(ws: WebSocket):
    print(f"opened: {ws}")


def run(id):
    ws = WebSocketApp(
        urljoin(WS_API_URL, id),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.recv_id = id
    print(f"running: {id}")
    ws.run_forever()


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        for recv_id in RECV_IDS:
            executor.submit(run, recv_id)

        executor.shutdown(wait=True)
