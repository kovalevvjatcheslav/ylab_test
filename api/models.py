from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


def get_multiple():
    return settings.MULTIPLE


class Currency(models.Model):
    title = models.CharField(max_length=10, unique=True)
    base = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='currencies')
    is_base = models.BooleanField(default=False)
    multiple = models.IntegerField(default=get_multiple)
    rate = models.DecimalField(decimal_places=2, max_digits=10, default=get_multiple)

    def clean(self):
        if self.is_base and (Currency.objects.filter(is_base=True).exists() or self.base is not None):
            raise ValidationError('Base currency already exists')


class Balance(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
