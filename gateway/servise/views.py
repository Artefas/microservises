from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import ast
import logging

# Create your views here.

from .conf import HOST_URL_ORDER
from .conf import HOST_URL_TRAIN
from .conf import HOST_URL_BILLING

from .servise_requests import TrainRequest
from .servise_requests import UserRequest
from .servise_requests import OrderRequest
from .servise_requests import BillingRequset

logger = logging.getLogger(__name__)

def byte_string_to_dict(data):
    try:
        assert isinstance(data, bytes), 'This is not byte string'
        assert data != b'', 'Byte string is empty'

        data = data.decode('utf-8')
        data = ast.literal_eval(data)
    except AssertionError as e:
        data = {}

    return data


class TrainView(View):
    def __init__(self, train_host_url = HOST_URL_TRAIN):
        self.trains = TrainRequest(train_host_url)

    def get(self, request, train_id = None):
        if train_id is None:
            params = dict(request.GET)
            return self.trains.trains_list(params=params)
        else:
            return self.trains.train_info(train_id=train_id)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def __init__(self, user_host_url = HOST_URL_ORDER):
        self.users = UserRequest(user_host_url)

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


class UserOrdersView(View):
    def __init__(self, user_host_url = HOST_URL_ORDER):
        self.users = UserRequest(user_host_url)

    def get(self, request, user_id):
        params = dict(request.GET)
        return self.users.user_orders_list(user_id=user_id, params=params)

@method_decorator(csrf_exempt, name='dispatch')
class BillingView(View):
    def __init__(
            self,
            billing_host_url = HOST_URL_BILLING,
            order_host_url = HOST_URL_ORDER
        ):
        self.billings = BillingRequset(billing_host_url)
        self.orders = OrderRequest(order_host_url)

    def post(self, request):
        data = byte_string_to_dict(request.body)
        order_id = data.get('order_id')
        resp_order = self.orders.order_confirm(order_id)
        resp_billing = self.billings.billing_create(data=data)

        data = {
            "billing" : {
                "status_code" : resp_billing.status_code,
                "content": byte_string_to_dict(resp_billing.content)
            },
            "order": {
                "status_code": resp_order.status_code,
                "content" : byte_string_to_dict(resp_order.content)
            }
        }

        return JsonResponse(data=data)

@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    def __init__(
            self,
            order_host_url = HOST_URL_ORDER,
            train_host_url = HOST_URL_TRAIN,
        ):
        self.orders = OrderRequest(order_host_url)
        self.trains = TrainRequest(train_host_url)

    def get(self, request, order_id = None):
        if order_id is None:
            params = dict(request.GET)
            return self.orders.order_list(params=params)
        else:
            resp_order = self.orders.order_info_json(order_id)
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
        resp_train = self.trains.set_places(train_id, ticket_count)
        resp_order = self.orders.order_create(data)

        resp_data = {
            "order": {
                "status_code" : resp_order.status_code,
                "content" : byte_string_to_dict(resp_order.content)
            },
            "train" : {
                "status_code" : resp_train.status_code,
                "content": byte_string_to_dict(resp_train.content)
            }
        }
        return JsonResponse(resp_data)







