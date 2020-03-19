from django.test import TestCase
from .tasks import update_rate


class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        update_rate()

    def test_signup(self):
        response = self.__signup(email='test@test.test', amount=100, currency='CZK')
        self.assertEqual(response.status_code, 200, msg=response.json())
        self.assertEqual(response.json(), {'ok': 'true'})

    def test_signin(self):
        self.__signup(email='test@test.test', amount=100, currency='CZK')
        response = self.__signin(email='test@test.test')
        self.assertEqual(response.status_code, 200, msg=response.json())
        self.assertEqual(response.json(), {'ok': 'true'})

    def test_transfer_same_currency(self):
        current_email = 'test@test.test'
        current_currency = 'CZK'
        target_currency = 'CZK'
        target_email = 'test1@test.test'
        response = self.__transfer(current_email, current_currency, target_email, target_currency)
        self.assertEqual(response.status_code, 200, msg=response.json())
        self.assertEqual(response.json(), {'ok': 'true'})

    def test_transfer_different_currency(self):
        current_email = 'test@test.test'
        current_currency = 'USD'
        target_currency = 'EUR'
        target_email = 'test1@test.test'
        response = self.__transfer(current_email, current_currency, target_email, target_currency)
        self.assertEqual(response.status_code, 200, msg=response.json())
        self.assertEqual(response.json(), {'ok': 'true'})

    def test_get_transactions(self):
        current_email = 'test@test.test'
        current_currency = 'USD'
        target_currency = 'EUR'
        target_email = 'test1@test.test'
        self.__transfer(current_email, current_currency, target_email, target_currency)
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 200, msg=response.json())
        self.assertEqual(response.json(), {'input': [], 'output': [{'to': 'test1@test.test', 'amount': '100.00'}]})

    def __signup(self, email, amount, currency):
        data = {'email': email, 'amount': amount, 'currency': currency, 'password': 'test'}
        return self.client.post('/api/signup/', data=data, content_type='application/json')

    def __signin(self, email):
        data = {'email': 'test@test.test', 'password': 'test'}
        return self.client.post('/api/signin/', data=data, content_type='application/json')

    def __transfer(self, current_email, current_currency, target_email, target_currency):
        self.__signup(email=current_email, amount=100, currency=current_currency)
        self.__signin(email=current_email)
        self.__signup(email=target_email, amount=100, currency=target_currency)
        data = {'targetEmail': target_email, 'amount': 100}
        return self.client.post('/api/transfer/', data=data, content_type='application/json')
