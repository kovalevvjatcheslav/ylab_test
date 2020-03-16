from django.test import TestCase
from .tasks import update_rate


class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        update_rate()

    def test_signup(self):
        response = self.client.post('/api/signup/')
        print(response.json())
