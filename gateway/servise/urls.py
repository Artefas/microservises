from django.conf.urls import url

from .apiviews import TrainAPIView
from .apiviews import UserAPIView
#from .apiviews import OrderAPIView
from .apiviews import UserOrdersAPIView
from .apiviews import BillingAPIView
from .apiviews import CreateOrderAPIView
from .apiviews import TokenAPIView
from .apiviews import AuthAPIView

app_name = 'servise'

urlpatterns = [
    url(r'^api/trains/$', TrainAPIView.as_view(), name='trains-list-api'),
    url(r'^api/trains/(?P<train_id>[0-9]+)/$', TrainAPIView.as_view(), name='train-detail-api'),

    #url(r'^api/users/$', UserAPIView.as_view(), name='users-list-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/$', UserAPIView.as_view(), name='user-detail-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/orders/$', UserOrdersAPIView.as_view(), name='user-orders-list-api'),
    url(r'^api/users/(?P<user_id>[0-9]+)/orders/(?P<order_id>[0-9]+)/$', UserOrdersAPIView.as_view(), name='user-order-detail-api'),

    url(r'^api/orders/$', CreateOrderAPIView.as_view(), name='order-create-api'),
    #url(r'^api/orders/(?P<order_id>[0-9]+)/$', OrderAPIView.as_view(), name='order-detail-api'),

    url(r'^api/billings/$', BillingAPIView.as_view(), name='billing-create-api'),
    url(r'^api/token/$', TokenAPIView.as_view(), name='token-api'),
    url(r'^api/auth/$', AuthAPIView.as_view(), name='auth-api')
]

from .apiviews import TrainListView
from .apiviews import TrainDetailView
from .apiviews import UserDetailView
from .apiviews import UserEditView
from .apiviews import UserOrdersView
from .apiviews import CreateOrderView
from .apiviews import OrderDetailView
from .apiviews import BillingView
from .apiviews import TokenView
from .apiviews import AuthView


urlpatterns += [
    url(r'^trains/$', TrainListView.as_view(), name='train-list'),
    url(r'^trains/(?P<train_id>[0-9]+)/$', TrainDetailView.as_view(), name='train-detail'),

    #url(r'^users/$', UserView.as_view(), name='users-list-api'),
    url(r'^user/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^user/edit$', UserEditView.as_view(), name='user-edit'),
    url(r'^user/orders/$', UserOrdersView.as_view(), name='user-orders-list'),

    url(r'^orders/$', CreateOrderView.as_view(), name='order-create'),
    url(r'^orders/(?P<order_id>[0-9]+)/$', OrderDetailView.as_view(), name='order-detail'),

    url(r'^billings/$', BillingView.as_view(), name='billing-create'),

    url(r'^token/$', TokenView.as_view(), name='token'),
    url(r'^auth/$', AuthView.as_view(), name='auth')
]

