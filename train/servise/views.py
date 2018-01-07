from rest_framework import generics

from .models import Train
from .serializers import TrainSerializer

class TrainList(generics.ListCreateAPIView):

    queryset = Train.objects.all()
    serializer_class = TrainSerializer

class TrainDetail(generics.RetrieveUpdateAPIView):

    queryset = Train.objects.all()
    serializer_class = TrainSerializer
