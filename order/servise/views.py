from rest_framework import generics
from django.http import HttpResponse

from .models import Order, User
from .serializers import OrderSerializer
from .serializers import UserSerializer
from .pagination  import MyPagination

class UserOrdersList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyPagination


    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs[self.lookup_url_kwarg]
        return self.queryset.filter(user_id = user_id)

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyPagination

class OrderDetail(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    lookup_url_kwarg = "order_id"
    lookup_field = "order_id"

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPagination

class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_url_kwarg = "user_id"
    lookup_field = "user_id"

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )


