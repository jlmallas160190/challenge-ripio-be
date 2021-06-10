import logging

from api.blockchain.serializers import (AccountSerializer, CoinSerializer,
                                        TransactionSerializer,
                                        WalletSerializer)
from app.blockchain.models import Coin, Transaction, Wallet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows coins to be viewed or edited.
    """
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallet to be viewed or edited.
    """
    queryset = Wallet.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def wallets(self, request,  pk=None, *args, **kwargs):
        try:
            if request.method == 'GET':
                queryset = Wallet.objects.filter(account_id=pk).all()
                serializer = WalletSerializer(queryset, many=True)
                return Response(serializer.data)
            if request.method == 'POST':
                data = request.data
                data['account_id'] = pk
                serializer = WalletSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'PUT':
                wallet = Wallet.objects.get(id=int(kwargs['wallet_id']))
                data = request.data
                serializer = WalletSerializer(wallet, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.error(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET', 'POST'])
    def transactions(self, request,  pk=None, *args, **kwargs):
        try:
            if request.method == 'GET':
                queryset = Transaction.objects.filter(sender_id=int(
                    kwargs['wallet_id']), sender__account_id=pk).all()
                serializer = TransactionSerializer(queryset, many=True)
                return Response(serializer.data)
            if request.method == 'POST':
                data = request.data
                data['sender_id'] = kwargs['wallet_id']
                serializer = TransactionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.error(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
