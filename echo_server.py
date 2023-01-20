import socket
from threading import Thread

# you cannot bind twice the  (address, port) combination
# port ranges (30000 - 60000) - 20000 cannot have more from a machine
# Port 8080 (8000 mark - not assigned - general applications)
# port 80 (Google), port 80 in the 8000 block, port 443 encrypted
# 8443 (encrypted app)

BYTES_TO_READ = 4096

HOST = "127.0.0.1"

PORT = 8080


def handle_connection(conn, addr):
    # Socket directly to the client
    # listen from the socket, connection comes in, new connection to that specific client, another socket to that client, differentiate between different clients, freeing up initial server socket
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)

            # Everything we send to it, we send it back since it's an ECHO server
            conn.sendall(data)

            # send does not guarantee all data, capture the number of bytes
            # sendall will return an error if it can't


def start_server():
    # auto closes some resources
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.listen()

# conn and address where it came from
        conn, addr = s.accept()

        handle_connection(conn, addr)


def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)

        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


start_server()
# start_threaded_server()
