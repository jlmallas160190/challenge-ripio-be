from django.db import models
from django.contrib.auth.models import User


class Coin(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre')
    currency = models.CharField(max_length=10, verbose_name="Divisa")

    def __str__(self):
        return self.name


class Account (models.Model):
    user = models.OneToOneField(User)


class Wallet (models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='wallets')
    coin = models.ForeignKey(
        Coin, on_delete=models.CASCADE, related_name="transactions")


class Transaction (models.Model):
    sender = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    recipient = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
