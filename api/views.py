from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User


class SignUp(View):

    def post(self, request, *args, **kwargs):
        return JsonResponse({'ok': 'true'})
