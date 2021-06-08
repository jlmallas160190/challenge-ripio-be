from app.blockchain.models import Coin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
