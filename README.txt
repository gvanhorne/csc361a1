# SmartClient - Python HTTP Client

## Overview

SmartClient is a Python-based HTTP client script that allows you to send HTTP GET requests to a given URL, receive and parse the server response, and print out various details from the response, including HTTP headers, cookies, and authorization status. It also supports following redirects and checking for HTTP/2 (h2) protocol support.

## Requirements

- Python 3.x
- The `ssl` module (usually included with Python standard libraries)

## Usage

To use SmartClient, follow these steps:

1. Download the SmartClient script.

2. Open a terminal or command prompt.

3. Navigate to the directory containing the SmartClient script.

4. Run the script with the desired URL as an argument:

    ```
    $ python3 SmartClient.py <URL>
    ```

    Replace `<URL>` with the URL you want to send the HTTP GET request to.

- Example:

    ```
    $ python3 SmartClient.py https://example.com
    ---Request Begin---
    GET / HTTP/1.1
    Host: example.com
    Connection: close

    ---Request End---
    HTTP request sent, awaiting response. . .

    ---Response headers---
    HTTP/1.1 200 OK
    Age: 252027
    Cache-Control: max-age=604800
    Content-Type: text/html; charset=UTF-8
    Date: Fri, 29 Sep 2023 23:31:49 GMT
    Etag: "3147526947+gzip+ident"
    Expires: Fri, 06 Oct 2023 23:31:49 GMT
    Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
    Server: ECS (sec/96ED)
    Vary: Accept-Encoding
    X-Cache: HIT
    Content-Length: 1256
    Connection: close

    ---Response body---
    {. . .Truncated. . .}

    website: example.com
    1. Supports http2: Yes
    2. List of cookies:
    No cookies set
    3. Password protected: No
    ```