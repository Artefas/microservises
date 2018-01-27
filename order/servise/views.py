from rest_framework import generics
from django.http import HttpResponse

from .models import Order, User
from .serializers import OrderSerializer
from .serializers import UserSerializer
from .pagination  import MyPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication

from django.contrib.auth.models import User as User2
from rest_framework.authtoken.models import Token

for user in User2.objects.all():
    Token.objects.get_or_create(user=user)

class UserOrdersList(generics.ListAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyPagination

    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs[self.lookup_url_kwarg]
        return self.queryset.filter(user_id = user_id)

class OrderList(generics.ListCreateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyPagination

class OrderDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    lookup_url_kwarg = "order_id"
    lookup_field = "order_id"

class UserList(generics.ListCreateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPagination

class UserDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_url_kwarg = "user_id"
    lookup_field = "user_id"

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )


