from rest_framework import serializers

from .models import Train

class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = '__all__'