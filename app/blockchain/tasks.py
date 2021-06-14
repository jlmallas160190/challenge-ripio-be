from celery import shared_task
from app.blockchain.models import Wallet


@shared_task
def add(x, y):
    return x + y


@shared_task
def calculate_balance_task(pk , wallet_type):
    wallet = Wallet.objects.get(pk=pk)
    if wallet is not None:
        wallet.calculate_balance()
        wallet.save()
        return {wallet_type: wallet.id, 'wallet_balance': wallet.balance}
    return {'error': 'Error to process the transaction'}
