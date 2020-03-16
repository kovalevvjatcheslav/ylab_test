from django.test import TestCase, RequestFactory


class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.abc = 'abc'

    def test_signup(self):
        response = self.client.post('/api/signup/')
        print(response.json())
        print(self.abc)
