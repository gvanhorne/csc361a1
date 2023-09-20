import socket
import ssl
import sys
from urllib.parse import urlparse

def parse_url(url):
    """
    Parse a URL and extract its path and hostname.

    If the URL doesn't include a scheme, "http://" is added by default.

    Parameters:
    url (str): The URL to parse.

    Returns:
    tuple: A tuple containing the path and hostname.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme

    # Ensure the scheme is "http://" if it's missing
    if not scheme:
        parsed_url = urlparse(f"http://{url}", scheme='http')

    # Extract the scheme, path, and hostname
    path = parsed_url.path if parsed_url.path else "/"
    hostname = parsed_url.netloc

    return path, hostname

def send_get_request(url):
    """
    Send an HTTP GET request to a given URL and print the response.

    Parameters:
    url (str): The URL to which the request will be sent.

    Returns:
    None
    """
    # Parse the URL
    path, hostname = parse_url(url)

    # Create an SSL context to establish a secure connection
    context = ssl.create_default_context()

    # Create a socket and wrap it with SSL, specifying the server's hostname
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)

    try:
        # Connect to the server on port 443 (HTTPS)
        conn.connect((url, 443))

        # Send an HTTP GET request to the server
        # Construct the HTTP GET request with the 'Connection: Keep-Alive' header
        print('---Request Begin---')
        request = b"GET " + path.encode() + b" HTTP/1.1\r\n"
        request += b"Host: " + hostname.encode() + b"\r\n"
        request += b"Connection: Keep-Alive\r\n\r\n"
        print(request.decode("utf-8")[:-1])
        conn.send(request)
        print('---Request End---')
        print('HTTP request sent, awaiting response. . .\n')

        # Receive and print the server's response (up to 1024 bytes)
        print('---Response Header---')
        response = conn.recv(1024)
        print(response.decode("utf-8"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection when done
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 SmartClient.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    send_get_request(url)