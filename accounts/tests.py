from django.test import TestCase
from django.contrib.auth.models import User

class AccountsTest(TestCase):
    def setUp(self):
        self._username = 'testuser'
        self._password = 'test1234'
        self.user = User(username=self._username)
        self.user.set_password(self._password)
        self.user.save()
        
    def test_login(self):
        self.client.login(username=self._username, password=self._password)
        resp = self.client.get('/')
        self.assertEqual(resp.context['user'].username, self._username)

    def test_logout(self):
        self.test_login()
        self.client.logout()
        resp = self.client.get('/')
        self.assertNotEqual(resp.context['user'].username, self._username)

