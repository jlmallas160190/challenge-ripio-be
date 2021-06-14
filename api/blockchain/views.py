from app.blockchain.tasks import calculate_balance_task
import logging
from rest_framework.authtoken.models import Token

from api.blockchain.serializers import (AccountSerializer, CoinSerializer,
                                        TransactionSerializer,
                                        WalletSerializer)
from app.blockchain.models import Account, Coin, Transaction, Wallet
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


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallet to be viewed or edited.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __authorize(self, request):
        auth_header = request.META['HTTP_AUTHORIZATION']
        index = auth_header.find(' ')
        token = Token.objects.get(key=auth_header[index:].strip())
        return Account.objects.get(user_id=token.user_id)

    def list(self, request, *args, **kwargs):
        try:
            account = self.__authorize(request=request)
            queryset = Wallet.objects.filter(account_id=account.id).all()
            serializer = WalletSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            logging.error(ex)
            return Response({
                'message': str(ex),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            account = self.__authorize(request=request)
            data = request.data
            data['account_id'] = account.id
            serializer = WalletSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logging.error(ex)
            return Response({
                'message': str(ex),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            self.__authorize(request=request)
            wallet = Wallet.objects.get(id=pk)
            wallet.calculate_balance()
            data = request.data
            serializer = WalletSerializer(wallet, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.error(ex)
            return Response({
                'message': str(ex),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET', 'POST'])
    def transactions(self, request,  pk=None, *args, **kwargs):
        try:
            account = self.__authorize(request=request)
            if request.method == 'GET':
                queryset = Transaction.objects.filter(
                    sender_id=pk, sender__account_id=account.id).all()
                serializer = TransactionSerializer(queryset, many=True)
                return Response(serializer.data)
            if request.method == 'POST':
                data = request.data
                data['sender_id'] = pk
                wallet = Wallet.objects.get(pk=pk)
                if wallet is None:
                    return Response({
                        'message': 'The wallet with id %s not exists'.format(data['sender_id']),
                        'status': status.HTTP_400_BAD_REQUEST,
                    }, status=status.HTTP_400_BAD_REQUEST)

                wallet.calculate_balance()
                if wallet.balance < data['amount']:
                    return Response({
                        'message': 'You have not money in your wallet for this transaction.',
                        'status': status.HTTP_400_BAD_REQUEST,
                    }, status=status.HTTP_400_BAD_REQUEST)
                serializer = TransactionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    calculate_balance_task.delay(
                        data['recipient'], 'recipient')
                    calculate_balance_task.delay(
                        data['sender_id'], 'sender_id')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.error(ex)
            return Response({'status': status.HTTP_400_BAD_REQUEST,
                             'message': 'Error en los datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
