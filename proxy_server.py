import socket
from threading import Thread

# Accept request, relays them to some target,
# Sends response back to the client
# All requests go to google.com (proxy target)
# Proxy server
# Proxy client


BYTES_TO_READ = 4096

PROXY_SERVER_HOST = "127.0.0.1"

PROXY_SERVER_PORT = 8080


def send_request(host, port, request_data):
    # client socket to make our request to Google
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Sending data to Google
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR)

        # Getting response from google
        data = client_socket.recv(BYTES_TO_READ)
        result = b''+data
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result


def handle_connection(conn, addr):
    with conn:
        print(f"Connected by: {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)

            # need the loop for 4 KB

            if not data:
                break

            print(data)

            # Send downstream to google, accumulating the data for the proxy server
            request += data

        response = send_request("www.google.com", 80, request)

        # Proxy will reply to the client
        conn.sendall(response)

    return


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # parameter 2 (socket documentation, parameter tells our program how much of a queue to allow)
        # connection is created, someone is trying to make a connection
        # keep that second connection in the queue, connection refused, queue
        server_socket.listen(2)

        conn, addr = server_socket.accept()

        handle_connection(conn, addr)

    return


def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # parameter 2 (socket documentation, parameter tells our program how much of a queue to allow)
        # connection is created, someone is trying to make a connection
        # keep that second connection in the queue, connection refused, queue
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


# start_server()

start_threaded_server()
