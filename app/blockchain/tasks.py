from celery import shared_task
from app.blockchain.models import Wallet


@shared_task
def add(x, y):
    return x + y


@shared_task
def calculate_balance_recipient(data):
    wallet = Wallet.objects.get(pk=data['recipient'])
    if wallet is not None:
        wallet.calculate_balance_by_recipient()
        wallet.save()
        return {'wallet_id': wallet.id, 'wallet_balance': wallet.balance}
