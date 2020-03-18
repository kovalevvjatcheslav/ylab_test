import json
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, AnonymousUser
from django.db.transaction import atomic
from jsonschema import validate
from .validation import sign_up_schema, sign_in_schema, transfer_schema
from .models import Currency, Balance, Transaction


class NotAuthorizedException(Exception):
    pass


def error_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotAuthorizedException as e:
            return JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return wrapper


class BaseView(View):
    @error_catcher
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SignUp(BaseView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        validate(data, sign_up_schema)
        user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password'])
        currency = Currency.objects.get(title=data['currency'].upper())
        Balance.objects.create(amount=data['amount'], currency=currency, user=user)
        return JsonResponse({'ok': 'true'})


class SignIn(BaseView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        validate(data, sign_in_schema)
        user = authenticate(request, username=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'ok': 'true'})
        else:
            raise Exception("This user doesn't exist")


class Transfer(BaseView):
    @atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        if user == AnonymousUser():
            raise NotAuthorizedException("User doesn't authorized")
        data = json.loads(request.body)
        validate(data, transfer_schema)
        amount = data['amount']
        if amount > user.balance.amount:
            raise Exception('Balance is low')
        target_user = User.objects.get(username=data['targetEmail'])
        user.balance.amount = user.balance.amount - amount
        user.balance.save()
        if target_user.balance.currency == user.balance.currency:
            target_amount = amount
        else:
            current_multiple = user.balance.currency.multiple
            target_rate = target_user.balance.currency.rate
            target_multiple = target_user.balance.currency.multiple
            current_rate = user.balance.currency.rate
            target_amount = amount*current_multiple*target_rate/(target_multiple*current_rate)
        target_user.balance.amount = target_user.balance.amount + target_amount
        target_user.balance.save()
        Transaction.objects.create(from_user=user, to_user=target_user, from_amount=amount, to_amount=target_amount)
        return JsonResponse({'ok': 'true'})
