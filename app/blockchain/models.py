from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum


class Coin(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre')
    currency = models.CharField(max_length=10, verbose_name="Divisa")

    def __str__(self):
        return self.name


class Account (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Wallet (models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,  validators=[
                                  MinValueValidator(Decimal('0.01'))])
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='wallets')
    coin = models.ForeignKey(
        Coin, on_delete=models.CASCADE, related_name="transactions")

    def __calculate_sent(self):
        total = Transaction.objects.filter(
            sender_id=self.pk).all().aggregate(Sum('amount'))
        if total['amount__sum'] is not None:
            return round(total['amount__sum'], 2)
        return Decimal("0.0")

    def __calculate_received(self):
        total = Transaction.objects.filter(
            recipient=self.pk).all().aggregate(Sum('amount'))
        if total['amount__sum'] is not None:
            return round(total['amount__sum'], 2)
        return Decimal("0.0")

    def calculate_balance(self):
        self.balance = self.__calculate_received() - self.__calculate_sent()


class Transaction (models.Model):
    sender = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    recipient = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, validators=[
                                 MinValueValidator(Decimal('0.01'))])
