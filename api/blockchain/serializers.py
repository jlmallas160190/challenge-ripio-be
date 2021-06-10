from app.blockchain.models import Account, Coin, Wallet
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField(write_only=True,)
    coin_id = serializers.IntegerField(write_only=True,)
    coin = CoinSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['coin_id', 'account_id', 'balance', 'coin']
