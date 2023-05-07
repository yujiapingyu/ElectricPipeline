import requests
import sys

def post_local(port, path, data):
    url = 'http://127.0.0.1:{}/{}'.format(port, path)
    response = requests.post(url, json=data)
    print(response.status_code)
    print(response.text)
    
if __name__ == '__main__':
    task = sys.argv[1]
    post_local(5000, 'create_task', {'task': task})