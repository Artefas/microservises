from rest_framework import serializers

from .models import Order, User

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'