from django.http import HttpResponse

import requests

class BaseRequest:

    def __init__(self, host_url):
        self.host_url = host_url

    def _response(self, response):
        return HttpResponse(
            status= response.status_code,
            content_type=response.headers.get('Content-Type'),
            content=response.content
        )

    def get(self, query_string = "", params = None):
        response = requests.get(self.host_url + query_string, params=params)
        return self._response(response)

    def post(self, query_string, data):
        response = requests.post(self.host_url + query_string, json=data)
        return self._response(response)

    def patch(self, query_string, data):
        response = requests.patch(self.host_url + query_string, json=data)
        return self._response(response)

    def delete(self, query_string):
        response = requests.delete(self.host_url + query_string)
        return self._response(response)

    def get_one_json(self, query_string):
        response = requests.get(self.host_url + query_string)
        return response.json()


class TrainRequest(BaseRequest):

    def trains_list(self, params):
        return self.get('trains/', params=params)

    def train_info(self, train_id):
        return self.get('trains/%s/' % train_id)

    def train_info_json(self, train_id):
        return self.get_one_json('trains/%s/' % train_id)


    def set_places(self, train_id, boughted_places):
        data = self.train_info_json(train_id)

        free_places = data.pop('free_places')
        free_places -= boughted_places

        resp_data = {
            "free_places": free_places
        }

        return self.patch('trains/%s/' % train_id, data= resp_data)

    def free_places(self, train_id, boughted_places):
        data = self.train_info_json(train_id)

        free_places = data.pop('free_places')
        free_places += boughted_places

        resp_data = {
            "free_places": free_places
        }
        return self.patch('trains/%s/' % train_id, resp_data)


class UserRequest(BaseRequest):

    def user_create(self, data):
        return self.post('users/', data=data)

    def user_update(self, user_id, data):
        return self.patch('users/%s/' % user_id, data=data)

    def users_list(self, params):
        return self.get('users/', params=params)

    def user_info(self, user_id):
        return self.get('users/%s/' % user_id)

    def user_info_json(self, user_id):
        return self.get_one_json('users/%s/' % user_id)

    def user_orders_list(self, user_id, params):
        return self.get('users/%s/orders/' % user_id, params=params)


class BillingRequset(BaseRequest):

    def billing_create(self, data):
        return self.post('billings/', data=data)


class OrderRequest(BaseRequest):

    def order_list(self, params):
        return self.get('orders/', params=params)

    def order_info(self, order_id):
        return self.get('orders/%s/' % order_id)

    def order_info_json(self, order_id):
        return self.get_one_json('orders/%s/' % order_id)

    def order_confirm(self, order_id):
        data = {
            "state": 1
        }
        return self.patch('orders/%s/' % order_id, data=data)

    def order_cancel(self, order_id):
        data = {
            "state": 2
        }
        return self.patch('orders/%s/' % order_id, data=data)

    def order_create(self, data):
        return self.post('orders/', data=data)






