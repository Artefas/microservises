from django.conf.urls import url

from .apiviews import TrainAPIView
from .apiviews import UserAPIView
#from .apiviews import OrderAPIView
from .apiviews import UserOrdersAPIView
from .apiviews import BillingAPIView

app_name = 'servise'

urlpatterns = [
    url(r'^api/trains/$', TrainAPIView.as_view(), name='trains-list-api'),
    url(r'^api/trains/(?P<train_id>[0-9]+)/$', TrainAPIView.as_view(), name='train-detail-api'),

    url(r'^api/users/$', UserAPIView.as_view(), name='users-list-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/$', UserAPIView.as_view(), name='user-detail-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/orders/$', UserOrdersAPIView.as_view(), name='user-orders-list-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/orders/(?P<order_id>[0-9]+)/$', UserOrdersAPIView.as_view(), name='user-order-detail-api'),

    #url(r'^api/orders/$', OrderAPIView.as_view(), name='orders-list-api'),
    #url(r'^api/orders/(?P<order_id>[0-9]+)/$', OrderAPIView.as_view(), name='order-detail-api'),

    url(r'^api/billings/$', BillingAPIView.as_view(), name='billing-create-api')
]

from .apiviews import TrainListView
from .apiviews import TrainDetailView
from .apiviews import UserDetailView
from .apiviews import UserEditView
from .apiviews import UserOrdersView


urlpatterns += [
    url(r'^trains/$', TrainListView.as_view(), name='train-list'),
    url(r'^trains/(?P<train_id>[0-9]+)/$', TrainDetailView.as_view(), name='train-detail'),

    #url(r'^users/$', UserView.as_view(), name='users-list-api'),
    url(r'^users/(?P<user_id>[0-9]+)/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^users/(?P<user_id>[0-9]+)/edit$', UserEditView.as_view(), name='user-edit'),
    url(r'^users/(?P<user_id>[0-9]+)/orders/$', UserOrdersView.as_view(), name='user-orders-list-api'),

    #url(r'^orders/$', OrderView.as_view(), name='orders-list-api'),
    #url(r'^orders/(?P<order_id>[0-9]+)/$', OrderView.as_view(), name='order-detail-api'),

    #url(r'^billings/$', BillingView.as_view(), name='billing-create-api')
]

