from rest_framework import generics
from django.http import HttpResponse

from .models import Train
from .serializers import TrainSerializer
from .pagination  import TrainPagination


from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

class TrainList(generics.ListCreateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    pagination_class = TrainPagination

class TrainDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Train.objects.all()
    serializer_class = TrainSerializer

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )
