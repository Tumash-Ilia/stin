from django import forms
from allauth.account.forms import SignupForm, LoginForm

from bank.models import Account


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


CURRENCIES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('CZK', 'CZK'),
    ('GBP', 'GBP'),
    ('CNY', 'CNY'),
)


class TransactionForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=True,
    )
    currency = forms.ChoiceField(
        label='Currency',
        choices=CURRENCIES,
        required=True,
    )
    method = forms.ChoiceField(
        label='Method',
        choices=(
            ('deposit', 'Deposit'),
            ('withdraw', 'Withdraw'),
        ),
        required=True,
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        # method = self.cleaned_data['method']
        if amount <= 0:
            raise forms.ValidationError("The amount must be greater than zero.")
        return amount
