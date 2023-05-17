from django.urls import path
from bank import views
from bank.views import AccountListView, TransactionView

urlpatterns = [
    path('', views.SimpleTemplateView.as_view()),
    path('overview/', AccountListView.as_view(), name='account_list'),
    path('payment/', TransactionView.as_view(), name='payment_view'),
]










