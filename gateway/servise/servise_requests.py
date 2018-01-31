from django.http import HttpResponse

import requests
from requests.auth import HTTPBasicAuth
import json

from rest_framework import status
from . import conf
from .conf import CLIENT_ID
from .conf import CLIENT_SECRET
from .conf import CLIENT_ID_JSON
from .conf import CLIENT_SECRET_JSON

from .conf import HOST_URL_AGGRIGATION

from .conf import SUCCESS_CHECK

class BaseRequest:
    def __init__(
            self,
            host_url,
            servise_name = 'base-name',
            app_id = conf.app_id,
            app_secret = conf.app_secret
    ):
        self.host_url = host_url
        self._servise_name = servise_name
        self._app_id = app_id
        self._app_secret = app_secret
        self.token = None


    def get_token(self):
        r = requests.post(self.host_url + 'token/', {"username":self._app_id, "password":self._app_secret})
        r = r.json()
        self.token = r.get('token')


    @property
    def headers(self):
        return {"Authorization": "Token %s" % self.token}


    def get(self, query_string = "", params = None, headers = None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        response = requests.get(self.host_url + query_string, params=params, headers=headers)
        if response.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            response = requests.get(self.host_url + query_string, params=params, headers=headers)
        return response


    def post(self, query_string, data, auth=None, headers = None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        response = requests.post(self.host_url + query_string, json=data , auth=auth, headers=headers)
        if response.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            response = requests.post(self.host_url + query_string, json=data, auth=auth, headers=headers)
        return response


    def patch(self, query_string, data, auth=None, headers = None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        response = requests.patch(self.host_url + query_string, json=data, auth=auth, headers=headers)
        if response.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            response = requests.patch(self.host_url + query_string, json=data, auth=auth, headers=headers)
        return response


    def delete(self, query_string, headers = None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        response = requests.delete(self.host_url + query_string, headers=headers)
        if response.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            response = requests.delete(self.host_url + query_string, headers=headers)
        return response


    def get_one_json(self, query_string, headers = None):
        if headers:
            if not headers.get("Authorization"):
                headers["Authorization"] = "Token %s" % self.token
        else:
            headers = self.headers
        response = requests.get(self.host_url + query_string, headers=headers)
        if response.status_code == 401:
            self.get_token()
            headers["Authorization"] = "Token %s" % self.token
            response = requests.get(self.host_url + query_string,  headers=headers)
        return response.status_code ,response.json()



class TrainRequest(BaseRequest):

    def check(self):
        return self.get()

    def trains_list(self, params):
        return self.get('trains/', params=params)

    def train_info(self, train_id):
        return self.get('trains/%s/' % train_id)

    def train_info_json(self, train_id):
        return self.get_one_json('trains/%s/' % train_id)

    def set_places(self, train_id, bought_places):
        status_code, data = self.train_info_json(train_id)

        free_places = data.pop('free_places')
        free_places -= bought_places

        resp_data = {
            "free_places": free_places
        }

        return self.patch('trains/%s/' % train_id, data = resp_data)

    def free_places(self, train_id, bought_places):
        status_code, data = self.train_info_json(train_id)

        free_places = data.pop('free_places')
        free_places += bought_places

        resp_data = {
            "free_places": free_places
        }
        return self.patch('trains/%s/' % train_id, resp_data)


class UserRequest(BaseRequest):

    def check(self):
        return self.get()

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

    def check(self):
        return self.get()

    def billing_create(self, data):
        return self.post('billings/', data=data)

    def billing_info_by_oreder_id(self, order_id):
        return self.get('billings/order/%s' % order_id)

    def billing_info_by_oreder_id_json(self, order_id):
        return self.get_one_json('billings/order/%s' % order_id)


class OrderRequest(BaseRequest):
    def check(self):
        return self.get()

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



class AuthRequester(BaseRequest):

    def get_user(self, access_token):
        headers = {'Authorization': 'Bearer %s' % access_token}
        response = self.get('user', headers=headers)
        return response

    def authorize(self, username, password):
        next = self.create_authorization_link_json()
        url = "http://localhost:8065/accounts/login/"
        print(username)
        print(password)
        data = {
            'username': username,
            'password': password,
            'next': next
        }
        response = requests.post(url,data, auth=(username,password), allow_redirects=True)
        return response

    def check_access_token(self, access_token):
        headers = {'Authorization': 'Bearer %s' % access_token}
        check = self.get('secret', headers=headers)
        return check.text == SUCCESS_CHECK

    def check_access_token_json(self, access_token):
        headers = {'Authorization': 'Bearer %s' % access_token}
        check = self.get('secret', headers=headers)
        return check.text == SUCCESS_CHECK

    def create_authorization_link(self):
        return self.host_url + 'o/authorize/?state=random_state_stringfgsfds&client_id=%s&response_type=code' % CLIENT_ID

    def create_authorization_link_json(self, client_id):
        return self.host_url + 'o/authorize/?state=random_state_stringfgsfds&client_id=%s&response_type=code' % client_id

    def get_token_oauth(self, code, redirect_uri):
        post_json = {'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri}
        response = requests.post(self.host_url + 'o/token/', post_json, auth=(CLIENT_ID, CLIENT_SECRET))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')

    def get_token_oauth_json(self, code, redirect_uri, client_id, client_secret):
        post_json = {'code': code, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri}
        response = requests.post(self.host_url + 'o/token/', post_json, auth=(client_id, client_secret))
        return response

    def refresh_token(self, refresh_token):
        post_json = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        response = requests.post(self.host_url + 'o/token/', post_json, auth=(CLIENT_ID, CLIENT_SECRET))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')

    def refresh_token_json(self, refresh_token):
        post_json = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        response = requests.post(self.host_url + 'o/token/', post_json, auth=(CLIENT_ID_JSON, CLIENT_SECRET_JSON))
        answer = response.json()
        return answer.get('access_token'), answer.get('refresh_token')







