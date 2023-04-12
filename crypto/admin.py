from django.contrib import admin

from crypto.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'public_key')
    search_fields = ('public_key', 'id')
