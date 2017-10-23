import http.client

import requests


def patch_send():
    old_send = http.client.HTTPConnection.send

    def new_send(self, data):
        print(data.decode())
        return old_send(self, data)
    http.client.HTTPConnection.send= new_send
patch_send()


def print_response(res):
    print('HTTP/1.1 {status_code}\n{headers}\n\n{body}'.format(
        status_code=res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.content,
    ))


response = requests.get("http://www.python.org")
print_response(response)
