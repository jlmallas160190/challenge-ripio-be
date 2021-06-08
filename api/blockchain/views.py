from api.blockchain.serializers import CoinSerializer
from app.blockchain.models import Coin
from rest_framework import permissions, viewsets

class CoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows coins to be viewed or edited.
    """
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticated]
