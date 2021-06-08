from app.blockchain.models import Coin
from rest_framework import serializers

class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
