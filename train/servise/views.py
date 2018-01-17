from rest_framework import generics
from django.http import HttpResponse

from .models import Train
from .serializers import TrainSerializer
from .pagination  import TrainPagination

class TrainList(generics.ListCreateAPIView):

    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    pagination_class = TrainPagination

class TrainDetail(generics.RetrieveUpdateAPIView):

    queryset = Train.objects.all()
    serializer_class = TrainSerializer

def check(request):
    return HttpResponse(
        status=200,
        content_type='application/json'
    )
