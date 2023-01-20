import socket

# 4 kilobytes
BYTES_TO_READ = 4096

# More than 4 kilobytes
# 1. There are not 4 gigabytes of data to get
# 2. Inefficient memory, how it receives
# 3. 4 GB, networks suck, interrupted, requests will be corrupted, smaller more manageable byte size.
# / slash, index of the website
# Two newlines \n\n, http get request with single header, host field. HTTP server, differentiate between headers and body of requests
# host.encode encodes to bytes


def get(host, port):

    request_data = b"GET / HTTP/1.1\nHost: " + host.encode("utf-8") + b"\n\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send(request_data)

    s.shutdown(socket.SHUT_WR)

    result = s.recv(BYTES_TO_READ)

    while (len(result) > 0):
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close()


get("www.google.com", 80)
