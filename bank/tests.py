from django.test import TestCase

from . import models


class SimpleTest(TestCase):
    def test_first_object_in_db(self):
        # The object was created in a migration step
        obj1 = models.SimpleModel.objects.first()
        self.assertEqual(obj1.just_text, 'Text 1')

    def test_second_object_in_db(self):
        # The object was created in a migration step
        obj1 = models.SimpleModel.objects.get(pk=2)
        self.assertEqual(obj1.just_text, 'Text 2')


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import Account, Transaction
from djmoney.money import Money


class TransactionViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('payment_view')
        # Создаем счет пользователя в USD
        account = Account.objects.create(owner=self.user, balance_currency='USD', balance=Money(0, 'USD'))
        account = Account.objects.create(owner=self.user, balance_currency='EUR', balance=Money(0, 'EUR'))

    def test_form_valid_deposit(self):
        data = {
            'amount': '100.00',
            'currency': 'USD',
            'method': 'deposit',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/overview/')
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account.balance, Money(100, 'USD'))
        self.assertEqual(transaction.transaction_type, 'deposit')

    def test_form_valid_withdraw(self):
        account = Account.objects.get(owner=self.user, balance_currency='USD')
        account.balance += Money(200, 'USD')
        account.save()
        data = {
            'amount': '100.00',
            'currency': 'USD',
            'method': 'withdraw',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/overview/')
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account.balance, Money(100, 'USD'))
        self.assertEqual(transaction.transaction_type, 'withdraw')

    def test_form_invalid_insufficient_funds(self):
        account = Account.objects.create(owner=self.user, balance=Money(50, 'USD'))
        data = {
            'amount': '100.00',
            'currency': 'USD',
            'method': 'withdraw',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertFormError(response, 'form', None, 'Insufficient funds for withdrawal.')

    def test_form_valid_no_account(self):
        data = {
            'amount': '100.00',
            'currency': 'EUR',
            'method': 'deposit',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/overview/')
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertNotEqual(transaction.account.balance, Money(100, 'CZK'))  # Check conversion to CZK
        self.assertEqual(transaction.transaction_type, 'deposit')
