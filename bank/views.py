from django.views.generic import TemplateView, ListView, FormView

from . import models
from .models import Account


# from django.shortcuts import render
# from .forms import TransactionForm


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
