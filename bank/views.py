from django.views.generic import TemplateView, ListView, FormView
from djmoney.money import Money
from . import models
from .models import Account
from .forms import TransactionForm
from django.shortcuts import get_object_or_404, redirect


class SimpleTemplateView(TemplateView):
    template_name = "bank/simple_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_data'] = models.SimpleModel.objects.all()
        return context


class AccountListView(ListView):
    model = Account
    template_name = 'bank/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class TransactionView(FormView):
    template_name = 'bank/transaction.html'
    form_class = TransactionForm
    success_url = '/overview/'

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        currency = form.cleaned_data['currency']
        method = form.cleaned_data['method']
        amount_money = Money(amount, currency)

        user = self.request.user

        account = get_object_or_404(Account, owner=user, balance_currency=currency)

        if method == 'deposit':
            account.balance += amount_money
        elif method == 'withdraw':
            if account.balance >= amount_money:
                account.balance -= amount_money
            else:
                # Обработка случая, когда недостаточно средств на счете
                # Можно выбросить исключение или вернуть сообщение об ошибке
                pass

        account.save()

        return redirect(self.success_url)
