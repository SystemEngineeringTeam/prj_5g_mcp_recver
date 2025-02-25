import sys
import time
import socket
from urllib.parse import urljoin
from websocket import WebSocket, WebSocketApp
from concurrent.futures import ThreadPoolExecutor

SEND_PORT = 12352
RECV_IDS = [1]
WS_API_URL = "wss://prj-5g-with-mocopi.sysken.net/ws/"
ADDRESS = sys.argv[1] if len(sys.argv) > 1 else None

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_timestamp = time.time()

def on_message(ws, data: bytes | str):
    recv_id = ws.recv_id

    splited_data = data.split("[:]".encode())
    motion_data = splited_data[0] if len(splited_data) > 1 else data
    timestamp = splited_data[1].decode() if len(splited_data) > 1 else time.time()

    print(f"received[{recv_id}]: {timestamp}")
    print(f"timestamp: {timestamp}")

    if float(timestamp) < last_timestamp:
        print(f"skip: {timestamp}")

    s.sendto(motion_data, (ADDRESS, SEND_PORT))


def on_error(ws, error):
    print(f"error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"closed: [{close_status_code}] {close_msg}")


def on_open(ws: WebSocket):
    print(f"opened: {ws}")


def run(id):
    ws = WebSocketApp(
        urljoin(WS_API_URL, str(id)),
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
