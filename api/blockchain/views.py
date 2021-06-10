from api.blockchain.serializers import AccountSerializer, CoinSerializer, WalletSerializer
from rest_framework.decorators import action
from app.blockchain.models import Coin, Wallet
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions, viewsets


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

    @action(detail=True, methods=['GET', 'POST'])
    def wallets(self, request,  pk=None):
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
