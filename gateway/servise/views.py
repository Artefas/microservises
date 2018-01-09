from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import ast
import json
import logging

from rest_framework import status

from requests.exceptions import ConnectionError

# Create your views here.

from .conf import HOST_URL_ORDER
from .conf import HOST_URL_TRAIN
from .conf import HOST_URL_BILLING
from .conf import HOST_URL_USER

from .servise_requests import TrainRequest
from .servise_requests import UserRequest
from .servise_requests import OrderRequest
from .servise_requests import BillingRequset

from .project_queue import RequestThread
from .project_queue import store_request
from threading import Event

from django.urls import reverse

logger = logging.getLogger(__name__)

stopFlag = Event()
thread = RequestThread(stopFlag)
thread.start()


def byte_string_to_dict(data):
    try:
        assert isinstance(data, bytes), 'This is not byte string'
        assert data != b'', 'Byte string is empty'

        data = data.decode('utf-8')
        data.replace("true", "True")
        data = ast.literal_eval(data)
    except AssertionError as e:
        data = {}
    return data

class BaseView(View):
    def __init__(
            self,
            train_host_url = HOST_URL_TRAIN,
            order_host_url = HOST_URL_ORDER,
            user_host_url  = HOST_URL_USER,
            billings_host_url = HOST_URL_BILLING
        ):
        self.trains = TrainRequest(train_host_url, servise_name="trains")
        self.orders = OrderRequest(order_host_url, servise_name="orders")
        self.users  = UserRequest(user_host_url, servise_name="users")
        self.billings = BillingRequset(billings_host_url, servise_name="billings")

class TrainView(BaseView):

    def get(self, request, train_id = None):
        if train_id is None:
            params = dict(request.GET)
            return self.trains.trains_list(params=params)
        else:
            return self.trains.train_info(train_id=train_id)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(BaseView):

    def _check_data(self, data):
        attributes = ('name',)
        for attr in attributes:
            if not data.get(attr):
                return False
        return True

    def get(self, request, user_id = None):
        if user_id is None:
            params = dict(request.GET)
            return self.users.users_list(params=params)
        else:
            return self.users.user_info(user_id)

    def post(self, requset):
        data = byte_string_to_dict(requset.body)
        return self.users.user_create(data)

    def patch(self, request, user_id):
        data = byte_string_to_dict(request.body)
        return self.users.user_update(user_id, data)


class UserOrdersView(BaseView):

    def get(self, request, user_id):
        params = dict(request.GET)
        return self.users.user_orders_list(user_id=user_id, params=params)


@method_decorator(csrf_exempt, name='dispatch')
class BillingView(BaseView):

    def _check_data(self, data):
        attributes = ('name', 'card', 'order_id', 'price')
        for attr in attributes:
            if not data.get(attr, None):
                return False
        return True

    def post(self, request):
        data = byte_string_to_dict(request.body)
        order_id = data.get('order_id')
        resp_order = self.orders.order_confirm(order_id)

        if resp_order.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            return resp_order
        else:
            resp_billing = self.billings.billing_create(data=data)
            if resp_billing.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                resp_order = self.orders.order_cancel(order_id)

        if resp_order.status_code != status.HTTP_503_SERVICE_UNAVAILABLE \
                and resp_billing.status_code != status.HTTP_503_SERVICE_UNAVAILABLE:
            flag = True
        else:
            flag = False

        data = {
            "billing" : {
                "status_code" : resp_billing.status_code,
            },
            "order": {
                "status_code": resp_order.status_code,
            },
            "result" : "order accept" if flag else "order does not accept"
        }

        return JsonResponse(data=data)

@method_decorator(csrf_exempt, name='dispatch')
class OrderView(BaseView):

    def get(self, request, order_id = None):
        if order_id is None:
            params = dict(request.GET)
            return self.orders.order_list(params=params)
        else:
            resp_order = self.orders.order_info_json(order_id)
            if resp_order.get("error"):
                return self.orders._error_response(503, resp_order)
            train_id = resp_order.pop("train_id")
            resp_train = self.trains.train_info_json(train_id)

            resp_order["train"] = resp_train
            return JsonResponse(resp_order)

    def post(self, request):
        data = byte_string_to_dict(request.body)
        ticket_count = data.get("ticket_count")
        if not isinstance(ticket_count, int):
            ticket_count = int(ticket_count)

        train_id = data.get("train_id")

        resp_train_check = self.trains.check()
        resp_order_check = self.orders.check()

        if resp_train_check.status_code != 200 or resp_order_check.status_code != 200:
            store_request.put(("POST", "http://localhost:8000" + reverse('servise:orders-list'), data))
            resp_data = {
                "order": {
                    "status_code": 201
                },
                "train": {
                    "status_code": 200
                }
            }
            return JsonResponse(resp_data)
        else:
            resp_train = self.trains.set_places(train_id, ticket_count)
            resp_order = self.orders.order_create(data)

            resp_data = {
                "order": {
                    "status_code" : resp_order.status_code
                },
                "train" : {
                    "status_code" : resp_train.status_code
                }
            }
            return JsonResponse(resp_data)







