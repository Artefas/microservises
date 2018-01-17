import requests

from threading import Thread
from queue import Queue

store_request = Queue()

class RequestThread(Thread):
    def __init__(self, event):
        self.stopped = event
        super().__init__()

    def _repeat_request(self):

        if not store_request.empty():
            method, url, data = store_request.get()
            Requester.request(method, url, data)

    def run(self):
        while not self.stopped.wait(4):
            self._repeat_request()

class Requester:
    def request(method, url, data):
            if method == 'POST':
                return requests.post(url, json=data)
            elif method == 'PATCH':
                return requests.patch(url, json=data)
            elif method == 'PUT':
                return requests.put(url, json=data)
            else:
                return requests.delete(url)