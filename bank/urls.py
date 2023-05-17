from django.urls import path
from bank import views
from bank.views import AccountListView

urlpatterns = [
    path('', views.SimpleTemplateView.as_view()),
    path('overview/', AccountListView.as_view(), name='account_list'),

]










