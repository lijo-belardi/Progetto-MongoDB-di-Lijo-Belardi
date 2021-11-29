from django.contrib import admin
from .models import Profile, Order

class AdminProfile(admin.ModelAdmin):
    list_display = ["user"]

    class Meta:
        model = Profile


admin.site.register(Profile, AdminProfile)
admin.site.register(Order)