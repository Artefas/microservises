from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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

class BaseAPIView(View):

    def __init__(
            self,
            train_host_url = HOST_URL_TRAIN,
            order_host_url = HOST_URL_ORDER,
            user_host_url  = HOST_URL_USER,
            billings_host_url = HOST_URL_BILLING
        ):
        self.trains   = TrainRequest(train_host_url, servise_name="trains")
        self.orders   = OrderRequest(order_host_url, servise_name="orders")
        self.users    = UserRequest(user_host_url,   servise_name="users")
        self.billings = BillingRequset(billings_host_url, servise_name="billings")

    def _extract_params(self, query_set):
        params_name = ["page"]
        params = {}

        for param_name in params_name:
            param = query_set.get(param_name, None)
            if param : params[param_name] = param

        return params

    def _response(self, response):
        return HttpResponse(
            status       = response.status_code,
            content_type = response.headers.get('Content-Type'),
            content      = response.content
        )
    def _error_response(self, status_code = 503, description = None):
        return HttpResponse(
            status       = status_code,
            content      = json.dumps(description),
            content_type ='application/json'
        )

class TrainAPIView(BaseAPIView):

    def get(self, request, train_id = None):
        try:
            if train_id is None:
                params = self._extract_params(request.GET)
                response = self.trains.trains_list(params=params)
                return self._response(response)
            else:
                response = self.trains.train_info(train_id=train_id)
                return self._response(response)
        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)


@method_decorator(csrf_exempt, name='dispatch')
class UserAPIView(BaseAPIView):

    def get(self, request, user_id = None):
        try:
            if user_id is None:
                params = self._extract_params(request.GET)
                response = self.users.users_list(params=params)
                return self._response(response)
            else:
                response = self.users.user_info(user_id)
                return self._response(response)
        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            response = self.users.user_create(data)
            return self._response(response)

        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)

    def patch(self, request, user_id):
        try:
            data = json.loads(request.body.body.decode("utf-8"))
            response = self.users.user_update(user_id, data)
            return self._response(response)

        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)


class UserOrdersAPIView(BaseAPIView):

    def get(self, request, user_id):
        try:
            params = self._extract_params(request.GET)
            response = self.users.user_orders_list(user_id=user_id, params=params)
            return self._response(response)

        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)


@method_decorator(csrf_exempt, name='dispatch')
class BillingAPIView(BaseAPIView):

    def _check_data(self, data):
        attributes = ('name', 'card', 'order_id', 'price')
        for attr in attributes:
            if not data.get(attr, None):
                return False
        return True

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
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

        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        except Exception as e:
            description = {"error" : "inside gateway error"}
            return self._error_response(status_code=500, description=description)


class UserOrderAPIView(BaseAPIView):

    def get(self, request, user_id, order_id):
        try:
            response_order = self.orders.order_info(order_id)
        except ConnectionError as e:
            description = {"error" : "servise is not avalibale"}
            return self._error_response(status_code=503, description=description)

        response_order = response_order.json()
        train_id = response_order.pop("train_id")

        try:
            response_train = self.trains.train_info(train_id)
            response_train = response_train.json()
            response_order["train"] = response_train
        except ConnectionError as e:
            response_order["train"] = train_id

        return JsonResponse(response_order)


@method_decorator(csrf_exempt, name='dispatch')
class CreateOrderAPIView(BaseAPIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        ticket_count = data.get("ticket_count")
        if not isinstance(ticket_count, int):
            ticket_count = int(ticket_count)

        train_id = data.get("train_id")

        try:
            self.trains.check()
            self.orders.check()
        except ConnectionError as e:
            store_request.put(("POST", "http://localhost:8000" + reverse('servise:order-create-api'), data))
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



from django.shortcuts import render
from .forms import TrainForm

# рендеринг ------------------------------------------------------------------------

class BaseView(View):
    def __init__(
            self,
            train_host_url=HOST_URL_TRAIN,
            order_host_url=HOST_URL_ORDER,
            user_host_url=HOST_URL_USER,
            billings_host_url=HOST_URL_BILLING
    ):
        self.trains = TrainRequest(train_host_url, servise_name="trains")
        self.orders = OrderRequest(order_host_url, servise_name="orders")
        self.users = UserRequest(user_host_url, servise_name="users")
        self.billings = BillingRequset(billings_host_url, servise_name="billings")

    def _extract_params(self, query_set):
        params_name = ["page"]
        params = {}

        for param_name in params_name:
            param = query_set.get(param_name, None)
            if param : params[param_name] = param

        return params




class TrainListView(BaseView):
    def get(self, request):

        context = {}
        params = self._extract_params(request.GET)

        try:
            page = int(params.get("page", 1))
            response = self.trains.trains_list(params)

            if response.status_code == 200:
                response = response.json()
                trains     = response["results"]
                page_count = response["page_count"]
                context["trains"] = trains
                context["page_count"] = page_count
                context["page_range"] = range(1, page_count + 1)
                context["current_page"] = page

                if response.get("previous"):
                    context["previous_page"] = int(page) - 1
                if response.get("next"):
                    context["next_page"] = int(page) + 1

                return render(request, 'servise/train_list.html', context)
            else:
                status_code = response.status_code
                context['status_code'] = status_code
                context['error_short'] = "Ошибка запроса"
                context['error_description'] = "Операция отклонена, запрос передан с ошибкой."
                return render(request, 'servise/error.html', context, status=status_code)

        except ConnectionError as e:
            status_code = 503
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        except Exception as e:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            context['error_description'] = u"Что-то пошло не так, работоспособность будет восстановлена в ближайшее время"
            return render(request, 'servise/error.html', context, status=status_code)

class TrainDetailView(BaseView):
    def get(self, request, train_id):
        context = {}

        try:
            response = self.trains.train_info(train_id)

            if response.status_code == 200:
                response = response.json()
                context["train"] = response
                return render(request, 'servise/train_detail.html', context)
            else:
                status_code = response.status_code
                context['status_code'] = status_code
                context['error_short'] = "Ошибка запроса"
                context['error_description'] = "Операция отклонена, запрос передан с ошибкой."
                return render(request, 'servise/error.html', context, status=status_code)

        except ConnectionError as e:
            status_code = 503
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        except Exception as e:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            context['error_description'] = u"Что-то пошло не так, работоспособность будет восстановлена в ближайшее время"
            return render(request, 'servise/error.html', context, status=status_code)



from .forms import UserForm

class UserDetailView(BaseView):
    def get(self, request, user_id):
        context = {}

        try:
            response = self.users.user_info(user_id)

            if response.status_code == 200:
                response = response.json()
                form = UserForm(response)
                context["form"] = form
                context["user_id"] = user_id
                return render(request, 'servise/user_detail.html', context)
            else:
                status_code = response.status_code
                context['status_code'] = status_code
                context['error_short'] = "Ошибка запроса"
                context['error_description'] = "Операция отклонена, запрос передан с ошибкой."
                return render(request, 'servise/error.html', context, status=status_code)

        except ConnectionError as e:
            status_code = 503
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        except Exception as e:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            context['error_description'] = u"Что-то пошло не так, работоспособность будет восстановлена в ближайшее время"
            return render(request, 'servise/error.html', context, status=status_code)

from .forms import UserEditForm

@method_decorator(csrf_exempt, name='dispatch')
class UserEditView(BaseView):
    form_class = UserEditForm

    def get(self, request, user_id):
        context = {}
        name    = request.GET.get("name")
        context["user_id"] = user_id
        context["name"]    = name
        context["form"]    = self.form_class(initial={'user_id' : user_id, 'name' : name})

        return render(request, 'servise/user_edit.html', context)

    def post(self, request, user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data.copy()
                self.users.user_update(user_id, data)
                return HttpResponseRedirect(reverse('servise:user-detail', kwargs={"user_id" : user_id}))
            except ConnectionError as e:
                status_code = 503
                context = {}
                context['status_code'] = status_code
                context['error_short'] = u"Сервис недоступен"
                context['error_description'] = u"Сервис поездов временно недоступен"
                return render(request, 'servise/error.html', context, status=status_code)

        return render(request, 'servise/user_edit.html', {'form':form, 'user_id': user_id})



class UserOrdersView(BaseView):
    state = {0 : "Оформлятеся", 1 : "Оплачен", 2 : "Отменен"}

    def get(self, request, user_id):
        context = {}
        params = {}

        try:
            page = request.GET.get("page", 1)
            params["page"] = page
            response = self.users.user_orders_list(user_id=user_id, params=params)
            print(response.status_code)

            if response.status_code == 200:
                response = response.json()
                orders = response["results"]

                for order in orders:
                    order["state"] = self.state[order["state"]]

                    train_id = order.pop("train_id")
                    try:
                        response_train = self.trains.train_info(train_id)
                        order["train"] = response_train.json()

                    except ConnectionError as e:
                        order["train"] = {"train_id" : train_id}

                page_count = response["page_count"]

                context["orders"] = orders
                context["page_count"] = page_count
                context["page_range"] = range(1, page_count + 1)
                context["current_page"] = page

                if response.get("previous"):
                    context["previous_page"] = int(page) - 1
                if response.get("next"):
                    context["next_page"] = int(page) + 1

                return render(request, 'servise/user_orders_list.html', context)
            else:
                status_code = response.status_code
                context['status_code'] = status_code
                context['error_short'] = "Ошибка запроса"
                context['error_description'] = "Операция отклонена, запрос передан с ошибкой."
                return render(request, 'servise/error.html', context, status=status_code)

        except ConnectionError as e:
            status_code = 503
            context = {}
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        except Exception as e:
            status_code = 500
            context['status_code'] = status_code
            context['error_short'] = u"Внутреняя ошибка сервера"
            context['error_description'] = u"Что-то пошло не так, работоспособность будет восстановлена в ближайшее время"
            return render(request, 'servise/error.html', context, status=status_code)

@method_decorator(csrf_exempt, name='dispatch')
class CreateOrderView(BaseView):
    """
    def get(self, request):
        context = {}
        train_id = request.GET["train_id"]
        ticket_count = request.GET["ticket_count"]
        user_id = 1
        try:
            resp_train_servise = self.trains.train_info(train_id)
        except ConnectionError as e:
            status_code = 503
            context = {}
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)
        try:
            resp_users_servise = self.users.user_info(user_id)
        except ConnectionError as e:
            status_code = 503
            context = {}
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервиc c пользователями временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        if resp_train_servise.status_code == 200:
            if resp_users_servise.status_code == 200:
                train = resp_train_servise.json()
                user = resp_users_servise.json()
                context["user":user,"train":train, "ticket_count":ticket_count]
                return render(request, 'servise/create_order.html', context)

            else:
                status_code = resp_users_servise.status_code
                context['status_code'] = status_code
                context['error_short'] = u"Ошибка запроса"
                context['error_description'] = u"Такого пользователя нет"
                return render(request, 'servise/error.html', context, status=status_code)
        else:
            status_code = resp_users_servise.status_code
            context['status_code'] = status_code
            context['error_short'] = u"Ошибка запроса"
            context['error_description'] = u"Такого поезда нет"
            return render(request, 'servise/error.html', context, status=status_code)
    """


    def post(self, request):

        ticket_count = int(request.POST["ticket_count"])
        train_id = request.POST["train_id"]
        user_id = 1

        data = {
            "user_id": user_id,
            "train_id": train_id,
            "ticket_count": ticket_count
        }

        try:
            self.trains.check()
            self.orders.check()

        except ConnectionError as e:
            store_request.put(("POST", "http://localhost:8000" + reverse('servise:order-create-api'), data))
            status_code = 201
            context = {}
            context['status_code'] = status_code
            context['short_message'] = "Успех"
            context['message'] = "Заказ создан сучки. Перейдите на страницу заказов для оплаты"
            context['user_id'] = user_id
            return render(request, 'servise/success_create_order.html', context, status=status_code)

        response_train_servise = self.trains.set_places(train_id, ticket_count)
        response_order_servise = self.orders.order_create(data)

        status_code = 201
        context = {}
        context['status_code'] = status_code
        context['short_message'] = "Успех"
        context['message'] = "Заказ создан сучки. Перейдите на страницу заказов для оплаты."
        context['user_id'] = user_id
        return render(request, 'servise/success_create_order.html', context, status=status_code)


class OrderDetailView(BaseView):
    state = {0: "Оформлятеся", 1: "Оплачен", 2: "Отменен"}

    def get(self,request, order_id):
        try:
            response_order_servise = self.orders.order_info(order_id)
        except ConnectionError as e:
            status_code = 503
            context = {}
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис заказов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        order = response_order_servise.json()
        train_id = order["train_id"]
        try:
            response_train_servise = self.trains.train_info(train_id)
        except ConnectionError as e:
            status_code = 503
            context = {}
            context['status_code'] = status_code
            context['error_short'] = u"Сервис недоступен"
            context['error_description'] = u"Сервис поездов временно недоступен"
            return render(request, 'servise/error.html', context, status=status_code)

        train = response_train_servise.json()

        if order["state"] in (0, 2):
            order["confirm_order"] = True
        else:
            order["cancel_order"] = True

        order["state"] = self.state[order["state"]]

        context = {}
        context["order"] = order
        context["train"] = train

        return render(request, 'servise/order_detail.html', context)



from .forms import BillingForm


@method_decorator(csrf_exempt, name='dispatch')
class BillingView(BaseView):
    form_class = BillingForm

    def get(self, request):

        ticket_price = request.GET["ticket_price"]
        order_id = request.GET["order_id"]

        data = {
            "order_id": order_id,
            "price" : ticket_price
        }

        form = self.form_class(initial=data)

        context = {}
        context["form"] = form

        return render(request, "servise/create_billing.html", context)

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            data = {}
            data["order_id"] = form.cleaned_data["order_id"]
            data["price"] = form.cleaned_data["price"]
            data["card"] = form.cleaned_data["card"]
            data["name"] = form.cleaned_data["name"]
            order_id = form.cleaned_data["order_id"]
            try:
                response_order_servise = self.orders.order_confirm(order_id)
            except ConnectionError as e:
                status_code = 503
                context = {}
                context['status_code'] = status_code
                context['error_short'] = u"Сервис недоступен"
                context['error_description'] = u"Сервис заказов временно недоступен"
                return render(request, 'servise/error.html', context, status=status_code)

            try:
                response_billing_servise = self.billings.billing_create(data=data)
            except ConnectionError as e:
                response_order_servise = self.orders.order_cancel(order_id)
                status_code = 503
                context = {}
                context['status_code'] = status_code
                context['error_short'] = u"Сервис недоступен"
                context['error_description'] = u"Сервис для оплаты временно недоступен. Приносим свои извенения."
                return render(request, 'servise/error.html', context, status=status_code)

            status_code = 201
            context = {}
            context['status_code'] = status_code
            context['short_message'] = "Успех"
            context['message'] = "Оплата произведена. Благодарим за пользование нашим сервисом."
            return render(request, 'servise/success_create_billing.html', context, status=status_code)











































