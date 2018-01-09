from django.conf.urls import url

from .views import BillingList
from .views import BillingDetail
from .views import BillingByOrderId
from .views import check

urlpatterns = [
    url(r'^billings/(?P<pk>[0-9]+)/$', BillingDetail.as_view(), name='billing-detail'),
    url(r'^billings/$', BillingList.as_view(), name='billing-create'),
    url(r'^billings/order/(?P<order_id>[0-9]+/)$', BillingByOrderId.as_view(), name='billingByOrderId-detail'),
    url(r'^$', check, 'check-servise-working')
]