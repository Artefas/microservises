from django.conf.urls import url

from .views import TrainDetail
from .views import TrainList

urlpatterns = [
    url(r'^trains/(?P<pk>[0-9]+)/$', TrainDetail.as_view(), name='train-detail'),
    url(r'^trains/$', TrainList.as_view(), name='train-list')
]