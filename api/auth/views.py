
from api.auth.serializers import AccountRegisterSerializer
from app.blockchain.models import Account
from rest_framework import permissions
from rest_framework.generics import CreateAPIView


class AccountRegisterViewSet(CreateAPIView):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
