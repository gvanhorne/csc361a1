import urllib.request
import sys

def send_get_request(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_request_example.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    result = send_get_request(url)
    print(result)
