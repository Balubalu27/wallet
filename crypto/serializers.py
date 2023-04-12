from rest_framework import serializers

from crypto.accounts import get_account_balance
from crypto.models import CURRENCIES, Wallet


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wallet
        fields = ("id", "currency", "public_key", "balance")
        read_only_fields = ("id", "balance", "public_key")

    @staticmethod
    def get_balance(obj: Wallet):
        return get_account_balance(obj.public_key)


class TransactionSerializer(serializers.Serializer):
    send_from = serializers.CharField(max_length=255, write_only=True, help_text="Кошелеĸ отправителя")
    to = serializers.CharField(max_length=255, write_only=True, help_text="Кошелеĸ получателя")
    currency = serializers.ChoiceField(choices=CURRENCIES.choices, write_only=True, help_text="Валюта")
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, write_only=True, help_text="Сумма перевода"
    )
    hash = serializers.CharField(max_length=255, read_only=True, help_text="Хэш транзакции")
