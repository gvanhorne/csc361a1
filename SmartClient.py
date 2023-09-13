import urllib.request
import sys

def send_get_request(url):
    headers = {
        'Host': 'www.example.com',
        'Connection': 'Keep-Alive',
    }
    try:
        request = urllib.request.Request(url, headers=headers, method='GET')
        response = urllib.request.urlopen(request)
        return request, response
    except urllib.error.URLError as e:
        return None, str(e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 SmartClient.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    request, response = send_get_request(url)

    if request is not None:
        print(f"{request.get_method()} {request.full_url}")
        
        # Print any request headers if needed
        for header, value in request.headers.items():
            print(f"{header}: {value}")

    if response is not None:
        content = response.read().decode('utf-8')
        print(content)
    else:
        print("Error occurred while making the request.")
