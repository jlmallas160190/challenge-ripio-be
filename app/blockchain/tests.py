from decimal import Decimal
from app.blockchain.models import Account, Coin, Transaction, Wallet
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestCoinViewSet(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='test123')
        self.user.save()
        self.client.login(username="test", password="test123")

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.coin = Coin.objects.create(id=100, name="Coin Test", currency="$")
        self.coin.save()

    def test_create_coin_with_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/v1/blockchain/coins/', {
            "name": "Bitcoin",
            "currency": "$"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_coin_without_authenticate(self):
        response = self.client.post('/api/v1/blockchain/coins/', {
            "name": "Bitcoin",
            "currency": "$"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_coin_with_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put('/api/v1/blockchain/coins/{}/'.format(self.coin.id), {
            "name": "Bitcoin",
            "currency": "$"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_coin_with_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/v1/blockchain/coins/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_coin_without_authenticate(self):
        response = self.client.get('/api/v1/blockchain/coins/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTransactionViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='test123')
        self.user.save()
        self.client.login(username="test", password="test123")

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.coin = Coin.objects.create(id=100, name="Coin Test", currency="$")
        self.coin.save()

        self.account = Account.objects.create(user=self.user)
        self.account.save()

        self.wallet = Wallet.objects.create(
            id=100, account=self.account, coin=self.coin)
        self.wallet.save()

        userRecipient = User.objects.create_user(
            username='testRecipient', password='testRecipient123')
        userRecipient.save()

        accountRecipient = Account.objects.create(user=userRecipient)
        accountRecipient.save()

        self.walletRecipient = Wallet.objects.create(
            id=101, account=accountRecipient, coin=self.coin)
        self.walletRecipient.save()

        self.transaction = Transaction.objects.create(
            id=100, sender=self.walletRecipient, amount=Decimal('100'), recipient=self.wallet.pk)
        self.transaction.save()
        self.wallet.calculate_balance()

    def test_list_transaction_with_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(
            '/api/v1/blockchain/wallets/{}/transactions'.format(self.wallet.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction_with_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/v1/blockchain/wallets/{}/transactions'.format(self.wallet.id), {
            "amount": Decimal('1'),
            "recipient": self.walletRecipient.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_without_money(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/v1/blockchain/wallets/{}/transactions'.format(self.wallet.id), {
            "amount": Decimal('200'),
            "recipient": self.walletRecipient.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'You have not money in your wallet for this transaction, your balance is {}'.format(
            self.wallet.balance))
