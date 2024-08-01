import os
import socket

PORT = int(os.environ.get("PORT") or 65500)
SERVER = os.environ.get("ADDRESS") or "127.0.0.1"

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SERVER, PORT))

    try:
        while True:
            msg, address = s.recvfrom(8192)
            # print(f"[RECV] {address}: {msg}")
            print(msg)

    except KeyboardInterrupt:
        print("Finished!")


if __name__ == "__main__":
    main()
