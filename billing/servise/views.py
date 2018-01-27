from rest_framework import generics
from django.http import HttpResponse

from .models import Billing
from .serializers import BillingSerializer
from .pagination  import BillingPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

class BillingList(generics.ListCreateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    pagination_class = BillingPagination

class BillingDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

class BillingByOrderId(generics.RetrieveAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    pagination_class = BillingPagination

    lookup_field = "order_id"
    lookup_url_kwarg = "order_id"

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )
