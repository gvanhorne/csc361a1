import socket
import ssl
import sys

def send_get_request(url):
    """
    Send an HTTP GET request to a given URL and print the response.

    Parameters:
    url (str): The URL to which the request will be sent.

    Returns:
    None
    """
    # Create an SSL context to establish a secure connection
    context = ssl.create_default_context()

    # Create a socket and wrap it with SSL, specifying the server's hostname
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)

    try:
        # Connect to the server on port 443 (HTTPS)
        conn.connect((url, 443))

        # Send an HTTP GET request to the server
        request = b"GET / HTTP/1.1\r\n\r\n"
        conn.send(request)

        # Receive and print the server's response (up to 1024 bytes)
        response = conn.recv(1024)
        print(response)
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