from django.conf.urls import url

from .views import TrainView
from .views import UserView
from .views import OrderView
from .views import UserOrdersView
from .views import BillingView

app_name = 'servise'

urlpatterns = [
    url(r'^trains/$', TrainView.as_view(), name='trains-list'),
    url(r'^trains/(?P<train_id>[0-9]+)/$', TrainView.as_view(), name='train-detail'),

    url(r'^users/$', UserView.as_view(), name='users-list'),
    url(r'^users/(?P<user_id>[0-9]+)/$', UserView.as_view(), name='user-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/orders/$', UserOrdersView.as_view(), name='user-orders-list'),

    url(r'^orders/$', OrderView.as_view(), name='orders-list'),
    url(r'^orders/(?P<order_id>[0-9]+)/$', OrderView.as_view(), name='order-detail'),

    url(r'^billings/$', BillingView.as_view(), name='billing-create')
]