from django.urls import path

from crypto.views import TransactionView, WalletView

urlpatterns = [
    path('wallets/', WalletView.as_view(), name='wallets'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
]
