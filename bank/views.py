from django.views.generic import TemplateView, ListView, FormView
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money
from . import models
from .models import Account, Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SimpleTemplateView(TemplateView):
    template_name = "bank/simple_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_data'] = models.SimpleModel.objects.all()
        return context


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'bank/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class TransactionView(LoginRequiredMixin, FormView):
    template_name = 'bank/transaction.html'
    form_class = TransactionForm
    success_url = '/overview/'

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        currency = form.cleaned_data['currency']
        method = form.cleaned_data['method']
        amount_money = Money(amount, currency)

        user = self.request.user

        account = Account.objects.filter(owner=user, balance_currency=currency).first()

        if not account:
            # Если у пользователя нет счета в выбранной валюте,
            # выполняем конвертацию валюты в CZK
            czk_currency = 'CZK'
            amount_money = convert_money(amount_money, czk_currency)
            # account = Account.objects.create(user=user, currency=czk_currency, balance=czk_amount)
            account = get_object_or_404(Account, owner=user, balance_currency=czk_currency)

        if method == 'deposit':
            Transaction.objects.create(user=user, account=account, amount=amount, amount_currency=currency,
                                       transaction_type='deposit')
            account.balance += amount_money
            account.save()
        # elif method == 'withdraw':
        #     if account.balance >= amount_money:
        #         Transaction.objects.create(user=user, account=account, amount=amount, amount_currency=currency,
        #                                    transaction_type='withdraw')
        #         account.balance -= amount_money
        #         account.save()
        #     else:
        #         czk_currency = 'CZK'
        #         czk_amount_money = convert_money(amount_money, czk_currency)
        #
        #         czk_account = Account.objects.filter(owner=user, balance_currency=czk_currency).first()
        #
        #         if czk_account.balance >= czk_amount_money:
        #             Transaction.objects.create(user=user, account=czk_account, amount=amount, amount_currency=currency,
        #                                        transaction_type='withdraw')
        #             czk_account.balance -= czk_amount_money
        #             czk_account.save()
        #         else:
        #             form.add_error(None, "Insufficient funds for withdrawal.")
        #             return self.form_invalid(form)

        elif method == 'withdraw':
            if account.balance >= amount_money:
                Transaction.objects.create(user=user, account=account, amount=amount, amount_currency=currency,
                                           transaction_type='withdraw')
                account.balance -= amount_money
                account.save()
            else:
                ten_percent_balance = account.balance * 0.1
                if amount_money < (account.balance + ten_percent_balance):
                    Transaction.objects.create(user=user, account=account, amount=amount, amount_currency=currency,
                                               transaction_type='withdraw')
                    account.balance -= amount_money

                    account.balance += account.balance * 0.1
                    account.save()
                else:
                    czk_currency = 'CZK'
                    czk_amount_money = convert_money(amount_money, czk_currency)

                    czk_account = Account.objects.filter(owner=user, balance_currency=czk_currency).first()

                    if czk_account.balance >= czk_amount_money:
                        Transaction.objects.create(user=user, account=czk_account, amount=czk_amount_money,
                                                   amount_currency=czk_currency,
                                                   transaction_type='withdraw')
                        czk_account.balance -= czk_amount_money
                        czk_account.save()
                    else:
                        ten_percent_balance_czk = czk_account.balance * 0.1
                        if czk_amount_money < (czk_account.balance + ten_percent_balance_czk):
                            Transaction.objects.create(user=user, account=czk_account, amount=czk_amount_money,
                                                       amount_currency=czk_currency,
                                                       transaction_type='withdraw')
                            czk_account.balance -= czk_amount_money
                            czk_account.balance += czk_account.balance * 0.1
                            czk_account.save()
                        else:
                            form.add_error(None, "Insufficient funds for withdrawal.")
                            return self.form_invalid(form)

        return redirect(self.success_url)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'bank/transactions_list.html'
    context_object_name = 'transactions'
