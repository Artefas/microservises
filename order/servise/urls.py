from django.conf.urls import url

from .views import OrderDetail
from .views import OrderList
from .views import UserOrdersList
from .views import UserList
from .views import UserDetail
from .views import check

from rest_framework_expiring_authtoken import views as auth_views

urlpatterns= [
    url(r'^users/(?P<user_id>[0-9]+)/orders/$', UserOrdersList.as_view(), name='users_order-list'),
    url(r'^users/(?P<user_id>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^orders/(?P<order_id>[0-9]+)/$', OrderDetail.as_view(), name='order-detail'),
    url(r'^orders/$', OrderList.as_view(), name='order-list'),
    url(r'^$', check, name='check-servise-working'),

    url(r'^token/$', auth_views.obtain_expiring_auth_token)
]