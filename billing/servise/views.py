from rest_framework import generics
from django.http import HttpResponse

from .models import Billing
from .serializers import BillingSerializer

class BillingList(generics.ListCreateAPIView):

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

class BillingDetail(generics.RetrieveUpdateAPIView):

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

class BillingByOrderId(generics.RetrieveAPIView):

    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    lookup_field = "order_id"
    lookup_url_kwarg = "order_id"

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )
