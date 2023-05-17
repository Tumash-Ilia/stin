from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator


# Create your models here.

class SimpleModel(models.Model):
    just_text = models.CharField(
        verbose_name="Just a field",
        max_length=255
    )


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='CZK',
                         validators=[MinMoneyValidator(0)])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=10, decimal_places=2, validators=[MinMoneyValidator(0)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
