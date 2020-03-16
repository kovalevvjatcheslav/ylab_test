from django.conf import settings
from celery.task.base import periodic_task
from celery.schedules import crontab
import requests
from .models import Currency


@periodic_task(run_every=(crontab(minute=f'*/{settings.UPDATE_TIMEOUT}')))
def update_rate():
    response = requests.get(settings.RATES_API_URL)
    data = response.json()
    base, created = Currency.objects.get_or_create(title=data['base'], defaults={'is_base': True})
    for title, rate in data['rates'].items():
        currency, created = Currency.objects.get_or_create(title=title,
                                                           defaults={'base': base, 'rate': rate*settings.MULTIPLE})
        if not created:
            currency.base = base
            currency.rate = rate*settings.MULTIPLE
            currency.save()
    response = requests.get(settings.BITCOIN_RATE_URL)
    bitcoin_data = response.json()
    rate = bitcoin_data[base.title]['last']
    currency, created = Currency.objects.get_or_create(title='BTC',
                                                       defaults={'base': base, 'rate': rate * settings.MULTIPLE})
    if not created:
        currency.base = base
        currency.rate = rate * settings.MULTIPLE
        currency.save()
