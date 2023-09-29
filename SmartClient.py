import socket
import ssl
import sys

def print_authorization_status(response: str):
    """
    Print the authorization status based on the provided response.

    Args:
        response (str): The HTTP response message or status.

    Example:
        >>> response = '401 Unauthorized'
        >>> print_authorization_status(response)
        3. Password protected: yes

    This function checks the provided response message for common HTTP
    status codes related to authorization and prints whether the resource
    is password protected or not.
    """
    if '401 Unauthorized' in response:
        print("3. Password protected: yes")
    elif '403 Not authenticated' in response:
        print("3. Password protected: yes")
    elif '400 Forbidden' in response:
        print("3. Password protected: yes")
    else:
        print("3. Password protected: no")

def print_cookie_list(header_dict: dict):
    """
    Print a list of cookies from the given header dictionary.

    Args:
        header_dict (dict): A dictionary containing HTTP headers.

    Example:
        >>> header_dict = {'Set-Cookie': [{'cookie1': 'value1', 'Domain': 'example.com', 'HttpOnly': True},
        ...                                {'cookie2': 'value2', 'Path': '/path', 'Secure': True}]}

        >>> print_cookie_list(header_dict)
        2. List of cookies:
        cookie name: cookie1, cookie value: value1, Domain: example.com, HttpOnly: True
        cookie name: cookie2, cookie value: value2, Path: /path, Secure: True
    """
    print("2. List of cookies:")
    if 'Set-Cookie' in header_dict:
        for cookie in header_dict['Set-Cookie']:
            name_property_printed = False
            line = ""
            for attr, value in cookie.items():
                if not name_property_printed:
                    line += f"cookie name: {attr}, cookie value: {value}, "
                    name_property_printed = True
                else:
                    line += f"{attr}: {value}, "
            print(line.rstrip().rstrip(','))
    else:
        print('No cookies set')

def parse_set_cookie(set_cookie_str: str):
    """
    Parse a "Set-Cookie" header string into a dictionary of cookie attributes.

    Args:
        set_cookie_str (str): The string received from a "Set-Cookie" header.

    Returns:
        dict: A dictionary containing cookie attributes as key-value pairs.

    Example:
        >>> set_cookie_str = "myCookie=myValue; Domain=example.com; Expires=Wed, 21 Oct 2023 07:28:00 GMT; HttpOnly"
        >>> cookie_attributes = parse_set_cookie(set_cookie_str)
        >>> print(cookie_attributes)
        >>> {'myCookie': 'myValue', 'Domain': 'example.com', 'Expires': 'Wed, 21 Oct 2023 07:28:00 GMT', 'HttpOnly': True}
    """
    attributes = {}
    parts = set_cookie_str.split(';')

    for part in parts:
        key_value_pair = part.strip().split('=', 1)
        if len(key_value_pair) == 2:
            key, value = key_value_pair
            key = key.strip()
            value = value.strip()

            # Convert certain attribute values to their proper types
            if key.lower() == 'expires':
                value = value.strip()
            elif key.lower() == 'max-age':
                # Parse Max-Age attribute as an integer
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif key.lower() in ('httponly', 'secure', 'samesite'):
                # Parse HttpOnly, Secure, and SameSite attributes as boolean
                value = True

            attributes[key] = value

    return attributes

def check_http2_support(hostname: str):
    """
    Check if a given hostname supports HTTP/2 (h2) protocol.

    Args:
        hostname (str): The hostname or domain name to check for HTTP/2 support.

    Returns:
        str: Returns 'Yes' if the hostname supports HTTP/2 (h2) protocol,
             'No' otherwise.

    Example:
        result = check_http2_support("example.com")
        print(result)  # Output will be either 'Yes' or 'No' indicating HTTP/2 support.
    """
     # Parse the URL
    path, hostname = parse_url(url)

    # Create an SSL context to establish a secure connection
    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1', 'h2'])
    # Create a socket and wrap it with SSL, specifying the server's hostname
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    conn.connect((hostname, 443))
    protocol = conn.selected_alpn_protocol()
    if protocol == 'h2':
        return 'Yes'
    else:
        return 'No'

def parse_http_headers(headers_str: str):
    """
    Parse a string of HTTP headers into a dictionary.

    Args:
        headers_str (str): The string containing HTTP headers.

    Returns:
        dict: A dictionary where the keys are header names and the values are header values.

    Example:
        >>> headers_str = "Content-Type: text/html\r\nServer: Apache\r\nContent-Length: 123\r\n"
        >>> parsed_headers = parse_http_headers(headers_str)
        >>> print(parsed_headers)
        >>> {'Content-Type': 'text/html', 'Server': 'Apache', 'Content-Length': '123'}
    """
    headers = {}
    cookies = []
    lines = headers_str.split('\r\n')

    for line in lines:
        parts = line.split(': ', 1)
        if len(parts) == 2:
            key, value = parts
            if key in headers:
                # If the key already exists, check if it's "Set-Cookie"
                if key == 'Set-Cookie':
                    cookie_dict = parse_set_cookie(value)
                    cookies.append(cookie_dict)
                    headers[key] = cookies
                else:
                    # If it's not "Set-Cookie," store the value normally
                    headers[key] = value
            else:
                headers[key] = value

    return headers

def parse_url(url: str):
    """
    Parse a URL and extract its path and hostname.

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

    # Remove trailing '/' if it exists
    url = url.strip('/')
        
    # Split the URL into hostname and path
    parts = url.split("/", 1)
    if len(parts) == 1:
        hostname = parts[0]
        path = "/"
    else:
        hostname, path = parts
        path = f"/{path}"

    return f"{path}", f"{hostname}"

def decode_until_null(byte_string: bytes):
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

def send_request(url):
    """
    Send an HTTP GET request to a given URL and print details from the server response.

    Parameters:
    url (str): The URL to which the request will be sent.

    Returns:
    None
    """
    # Parse the URL
    path, hostname = parse_url(url)

    # Create an SSL context to establish a secure connection
    context = ssl.create_default_context()

    # Create a socket and wrap it with SSL
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    
    try:
        # Connect to the server on port 443 (HTTPS)
        conn.connect((hostname, 443))

        # Send an HTTP GET request to the server
        print('---Request Begin---')
        request = b"GET " + path.encode() + b" HTTP/1.1\r\n"
        request += b"Host: " + hostname.encode() + b"\r\n"
        request += b"Connection: close\r\n\r\n"
        print(request.decode()[:-1])
        conn.send(request)
        print('---Request End---')
        print('HTTP request sent, awaiting response. . .\n')

        full_msg = b""
        redirect = False
        header_dict = {}

        while True:
            response_chunk = conn.recv(1024)
            # Continue receiving until all chunks received
            if not response_chunk:
                # If there is a newline, must be we have both header and body
                if b"\r\n\r\n" in full_msg:
                    headers, body = full_msg.split(b"\r\n\r\n", 1)
                    print('---Response headers---')
                    header_dict = parse_http_headers(headers.decode())
                    if 'Location' in header_dict:
                        # We've been given a redirect location
                        # So use that once the entire message has been output
                        redirect = True
                    print(headers.decode())
                    print('---Response body---')
                    if b"\r\n" in body:
                        print(decode_until_null(body))
                    else:
                        print(body.decode())             
                else:
                    # Received no payload. So only print out the headers.
                    print('---Response headers---')
                    header_dict = parse_http_headers(full_msg.decode())
                    if 'Location' in header_dict:
                        redirect = True
                    print(full_msg.decode())
                    print('---Response body---')
                break
            full_msg += response_chunk

        # Now have all the information we need, so print out the required information
        print(f"website: {hostname}")
        http2_support = check_http2_support(hostname)
        print(f"1. Supports http2: {http2_support}")
        print_cookie_list(header_dict)
        print_authorization_status(full_msg.decode())
        if redirect:
            print(f"\r\n---Redirected to {header_dict['Location']}---\r\n")
            send_request(header_dict['Location'])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close out connection
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 SmartClient.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    send_request(url)