import socket
import ssl
import sys

def parse_url(url):
    """
    Parse a URL and extract its path and hostname.

    If the URL doesn't include a scheme, "http://" is added by default.

    Parameters:
    url (str): The URL to parse.

    Returns:
    tuple: A tuple containing the path and hostname.
    """
    # Check if the URL starts with "http://" or "https://"
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith('https://'):
        url = url[len("https://"):]
        
    # Split the URL into hostname and path
    parts = url.split("/", 1)
    if len(parts) == 1:
        hostname = parts[0]
        path = "/"
    else:
        hostname, path = parts

    return f"/{path}", f"{hostname}"

def decode_until_null(byte_string):
    """
    Decode a byte string until a null character (\x00) is encountered and remove trailing \r\n\r\n, if present.

    Args:
        byte_string (bytes): The input byte string to decode.

    Returns:
        str: The decoded text as a string.
    """
    decoded_text = ""
    for byte in byte_string:
        if byte == 0x00:
            break  # Stop decoding when null character is reached
        decoded_text += chr(byte)

    # Remove the trailing \r\n\r\n, if present
    if decoded_text.endswith("\n0\r\n\r\n"):
        decoded_text = decoded_text[:-6]

    return decoded_text

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
        conn.connect((hostname, 443))

        # Send an HTTP GET request to the server
        # Construct the HTTP GET request with the 'Connection: Keep-Alive' header
        print('---Request Begin---')
        request = b"GET " + path.encode() + b" HTTP/1.1\r\n"
        request += b"Host: " + hostname.encode() + b"\r\n"
        request += b"Connection: close\r\n\r\n"
        print(request.decode()[:-1])
        conn.send(request)
        print('---Request End---')
        print('HTTP request sent, awaiting response. . .\n')

        full_msg = b""
        while True:
            response_chunk = conn.recv(1024)
            if not response_chunk:
                if b"\r\n\r\n" in full_msg:
                    headers, body = full_msg.split(b"\r\n\r\n", 1)
                    print('---Response headers---')
                    print(headers.decode())
                    print('---Response body---')
                    if b"\r\n" in body:
                        print(decode_until_null(body))
                    else:
                        print(body.decode(encoding='utf-8', errors='ignore'))              
                else:
                    print('---Response headers---')
                    print(full_msg.decode())
                break
            full_msg += response_chunk

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