from django.contrib import admin
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('owner', 'balance')

    def currency(self, obj):
        return obj.balance
    currency.short_description = 'Currency'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'timestamp')
