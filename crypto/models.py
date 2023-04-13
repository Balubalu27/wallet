from django.db import models


class CURRENCIES(models.TextChoices):
    ETH = 'eth'


class Wallet(models.Model):
    currency = models.CharField(max_length=20, choices=CURRENCIES.choices, help_text="Валюта")
    public_key = models.CharField(max_length=255, unique=True, help_text="Публичный ĸлюч(адрес)")
    private_key = models.CharField(max_length=255, unique=True, help_text="Приватный ĸлюч")
