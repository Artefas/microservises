import requests

from threading import Thread
from queue import Queue

store_request = Queue()

class RequestThread(Thread):
    def __init__(self, event):
        self.stopped = event
        super().__init(self)

    def _repeat_request(self):

        if not store_request.empty():
            method, url, data = store_request.get()
            Requester.request(method, url, data)

    def run(self):
        while not self.stopped.wait(4):
            self._repeat_request()

class Requester:
    def stored_request(self, method, url, data):
        try:
            if method == 'POST':
                return requests.post(url, data=data)
            elif method == 'PATCH':
                return requests.patch(url, data=data)
            elif method == 'PUT':
                return requests.put(url,data=data)
            elif method == 'DELETE':
                return requests.delete(url)
            else:
                pass
        except ConnectionError:
            store_request.put(method, url, data)