import os
import socket

PORT = int(os.environ.get("PORT") or 65500)
SERVER = socket.gethostbyname(socket.gethostname())


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SERVER, PORT))

    try:
        while True:
            msg, address = s.recvfrom(8192)
            print(f"[RECV] {address}: {msg.decode()}")

    except KeyboardInterrupt:
        print("Finished!")


if __name__ == "__main__":
    main()
