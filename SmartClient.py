import socket
import ssl
import sys

def send_get_request(url):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)

    conn.connect((url, 443))

    conn.send(b"GET / HTTP/1.1\r\n\r\n")

    conn.send(b"GET / HTTP/1.1\r\n\r\n")

    print(conn.recv(1024))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 SmartClient.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    send_get_request(url)