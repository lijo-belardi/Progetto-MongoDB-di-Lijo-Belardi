from django.contrib import admin
from .models import Profile, Wallet, Order


class AdminProfile(admin.ModelAdmin):
    list_display = ["user", "_id", "ip_address", "last_login"]


class AdminOrder(admin.ModelAdmin):
    list_display = ["_id", "profile", "created", "status", "type"]


class AdminWallet(admin.ModelAdmin):
    list_display = ("user",
                    "_id",
                    "btc_wallet",
                    "usd_wallet",
                    "btc_balance",
                    "usd_balance")


admin.site.register(Profile, AdminProfile)
admin.site.register(Wallet, AdminWallet)
admin.site.register(Order, AdminOrder)