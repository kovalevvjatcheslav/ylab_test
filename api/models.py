from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Currency(models.Model):
    title = models.CharField(max_length=10)
    is_base = models.BooleanField()
    multiple = models.IntegerField(default=100)
    rate = models.DecimalField(decimal_places=2, max_digits=10)

    def clean(self):
        if self.is_base and Currency.objects.filter(is_base=True).exists():
            raise ValidationError('Base currency already exists')


class Balance(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
