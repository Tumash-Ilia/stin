from django.urls import path
from bank import views
from bank.views import AccountListView, TransactionView, TransactionListView

urlpatterns = [
    path('', views.SimpleTemplateView.as_view()),
    path('overview/', AccountListView.as_view(), name='account_list'),
    path('payment/', TransactionView.as_view(), name='payment_view'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
]










