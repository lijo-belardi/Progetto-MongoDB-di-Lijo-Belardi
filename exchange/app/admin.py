from django.contrib import admin
from .models import Profile, Wallet, OrderToBuy, OrderToSell


class AdminProfile(admin.ModelAdmin):
    list_display = ["user", "_id"]


class AdminOrderToBuy(admin.ModelAdmin):
    list_display = ["price", "quantity"]
    sortable_by = ["price"]


class AdminOrderToSell(admin.ModelAdmin):
    list_display = ["price", "quantity"]
    sortable_by = ["price"]


class AdminWallet(admin.ModelAdmin):
    list_display = ("user", "_id", "btc_wallet", "usd_wallet", "btc_balance", "usd_balance", "btc_available", "usd_available")


admin.site.register(Profile, AdminProfile)
admin.site.register(OrderToBuy, AdminOrderToBuy)
admin.site.register(OrderToSell, AdminOrderToSell)
admin.site.register(Wallet, AdminWallet)