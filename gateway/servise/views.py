from django.shortcuts import render
from django.views import View


from .conf import HOST_URL_ORDER
from .conf import HOST_URL_TRAIN
from .conf import HOST_URL_BILLING
from .conf import HOST_URL_USER

from .servise_requests import TrainRequest
from .servise_requests import UserRequest
from .servise_requests import OrderRequest
from .servise_requests import BillingRequset



